#!/usr/bin/env python3
"""Upload one video to YouTube from a job file. Secrets come from the environment; nothing secret is printed."""
import json, os, sys, urllib.request, urllib.parse, urllib.error
job = json.load(open(sys.argv[1]))
def post(url, data, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method='POST')
    return urllib.request.urlopen(req, timeout=120)
try:
    tok = json.load(post('https://oauth2.googleapis.com/token', urllib.parse.urlencode(dict(
        client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'],
        refresh_token=os.environ['YT_REFRESH_TOKEN'], grant_type='refresh_token')).encode()))['access_token']
except urllib.error.HTTPError as e:
    print('TOKEN ERROR', e.code, e.read().decode()[:400]); sys.exit(2)
if job.get('update_id'):  # change the privacy / schedule of a video that is already uploaded (no file needed)
    st = dict(privacyStatus=job.get('privacy', 'private'), selfDeclaredMadeForKids=False)
    if job.get('publish_at'): st['publishAt'] = job['publish_at']
    req = urllib.request.Request('https://www.googleapis.com/youtube/v3/videos?part=status', data=json.dumps(dict(id=job['update_id'], status=st)).encode(),
                                 headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'}, method='PUT')
    try:
        out = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        print('UPDATE ERROR', e.code, e.read().decode()[:600]); sys.exit(4)
    print('UPDATED id=%s privacy=%s publishAt=%s' % (out['id'], out['status']['privacyStatus'], out['status'].get('publishAt'))); sys.exit(0)
path = job.get('video_path')
if job.get('video_url'):
    path = '/tmp/video.mp4'; urllib.request.urlretrieve(job['video_url'], path)
size = os.path.getsize(path); print('video', path, size, 'bytes')
meta = dict(snippet=dict(title=job['title'][:100], description=job.get('description', ''), tags=job.get('tags', []), categoryId=str(job.get('category', 24))),
            status=dict(privacyStatus=job.get('privacy', 'private'), selfDeclaredMadeForKids=False))
if job.get('publish_at'):  # scheduled publish: YouTube needs privacy 'private' plus an RFC3339 publishAt time
    meta['status']['privacyStatus'] = 'private'; meta['status']['publishAt'] = job['publish_at']
auth = {'Authorization': 'Bearer ' + tok}
try:
    r = post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status', json.dumps(meta).encode(),
             dict(auth, **{'Content-Type': 'application/json; charset=UTF-8', 'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(size)}))
    loc = r.headers['Location']
    req = urllib.request.Request(loc, data=open(path, 'rb'), headers=dict(auth, **{'Content-Type': 'video/mp4', 'Content-Length': str(size)}), method='PUT')
    out = json.load(urllib.request.urlopen(req, timeout=3600))
except urllib.error.HTTPError as e:
    print('UPLOAD ERROR', e.code, e.read().decode()[:600]); sys.exit(3)
print('UPLOADED id=%s privacy=%s publishAt=%s url=https://youtu.be/%s' % (out['id'], out['status']['privacyStatus'], out['status'].get('publishAt'), out['id']))
print('channel', out['snippet'].get('channelTitle'), out['snippet'].get('channelId'))
