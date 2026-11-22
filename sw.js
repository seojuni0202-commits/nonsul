// 오프라인: 한 번 본 문제·그림·해설·라이브러리를 기기에 저장. 인터넷이 있으면 항상 최신본을 먼저 받는다.
const C='nsm-v1';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  const cdn=/(cdnjs\.cloudflare\.com|fonts\.googleapis\.com|fonts\.gstatic\.com)$/.test(u.hostname);
  if(cdn){e.respondWith(caches.open(C).then(async c=>{const hit=await c.match(r);if(hit)return hit;const res=await fetch(r);if(res.ok||res.type==='opaque')c.put(r,res.clone());return res}));return}
  if(u.origin!==location.origin)return;
  e.respondWith(caches.open(C).then(async c=>{const key=u.origin+u.pathname;
    try{const res=await fetch(r);if(res.ok)c.put(key,res.clone());return res}
    catch(err){const hit=await c.match(key);if(hit)return hit;throw err}}));
});
