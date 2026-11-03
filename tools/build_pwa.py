# Membangun paket PWA dari sumber artifact (dapur-nol.html). Jalankan ulang setiap kali sumber berubah.
import json, time, re, os
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
SRC=str(ROOT/"src"/"dapur-nol.html"); OUT=str(ROOT)
body=open(SRC).read()
title_m=re.search(r"<title>.*?</title>\n?",body); body=body.replace(title_m.group(0),"")
body=body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
ver=time.strftime("%Y%m%d-%H%M")
head=f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Dapur Nol</title>
<meta name="description" content="Panduan mengenal makanan dari nol: 100 resep pemula, 133 bahan dan bumbu, Kitchen Gems, dan tips belanja di pasar.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dapur Nol">
<meta property="og:title" content="Dapur Nol: panduan mengenal makanan dari nol">
<meta property="og:description" content="100 resep pemula, 133 bahan dan bumbu, tips belanja di pasar. Gratis, bisa dipasang di HP dan dibuka offline.">
<meta property="og:url" content="https://yaspip.github.io/dapur-nol/">
<meta property="og:image" content="https://yaspip.github.io/dapur-nol/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ilustrasi bawang putih, tomat, telur, dan cabai di atas talenan, dengan tulisan Dapur Nol">
<meta property="og:locale" content="id_ID">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5F1E8">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Dapur Nol">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''
tail=f'''
<script>
/* PWA: versi {ver}. Service worker mengambil versi terbaru setiap kali online, dan memakai salinan tersimpan saat offline. */
window.DAPUR_NOL_VERSION="{ver}";
if("serviceWorker" in navigator){{
  window.addEventListener("load",()=>{{navigator.serviceWorker.register("./sw.js").then(reg=>{{
    reg.addEventListener("updatefound",()=>{{const w=reg.installing;w&&w.addEventListener("statechange",()=>{{
      if(w.state==="installed"&&navigator.serviceWorker.controller){{try{{toast("Versi baru Dapur Nol siap. Tutup dan buka lagi aplikasinya.")}}catch(e){{}}}}
    }})}});
  }}).catch(()=>{{}})}});
}}
let deferredInstall=null;
window.addEventListener("beforeinstallprompt",e=>{{e.preventDefault();deferredInstall=e;
  if(document.getElementById("install-btn"))return;
  const b=document.createElement("button");b.id="install-btn";b.className="btn btn-ink";b.textContent="Pasang aplikasi";
  b.style.cssText="position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:65";
  b.onclick=async()=>{{b.remove();deferredInstall.prompt();try{{await deferredInstall.userChoice}}catch(_){{}}deferredInstall=null}};
  document.body.appendChild(b)}});
window.addEventListener("appinstalled",()=>{{document.getElementById("install-btn")?.remove()}});
</script>
</body>
</html>
'''
os.makedirs(OUT,exist_ok=True)
open(f"{OUT}/index.html","w").write(head+body+tail)
manifest={"name":"Dapur Nol","short_name":"Dapur Nol","description":"Panduan mengenal makanan dari nol: bahan, rasa, resep, dan belanja.",
 "lang":"id","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#F5F1E8","theme_color":"#F5F1E8",
 "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png"},
          {"src":"icons/maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}],
 "shortcuts":[{"name":"Resep","url":"./#resep"},{"name":"Belanja","url":"./#dapurku"},{"name":"Kitchen Gems","url":"./#gems"}]}
json.dump(manifest,open(f"{OUT}/manifest.webmanifest","w"),ensure_ascii=False,indent=1)
sw=f'''/* Dapur Nol service worker, versi {ver} */
const CACHE="dapurnol-{ver}";
const CORE=["./","./index.html","./manifest.webmanifest","./icons/icon-192.png","./icons/icon-512.png","./icons/maskable-512.png","./icons/apple-touch-icon.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("dapurnol-")&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{
  const req=e.request; if(req.method!=="GET")return;
  const url=new URL(req.url);
  // Halaman: ambil dari internet dulu (selalu versi terbaru), pakai salinan kalau offline.
  if(req.mode==="navigate"||(url.origin===location.origin&&url.pathname.endsWith(".html"))){{
    e.respondWith(fetch(req).then(r=>{{const cp=r.clone();caches.open(CACHE).then(c=>c.put("./index.html",cp));return r}}).catch(()=>caches.match("./index.html")));return;
  }}
  // Font Google dan file lain: pakai salinan dulu, perbarui di belakang.
  if(url.origin===location.origin||url.hostname.endsWith("fonts.googleapis.com")||url.hostname.endsWith("fonts.gstatic.com")){{
    e.respondWith(caches.match(req).then(hit=>{{const net=fetch(req).then(r=>{{if(r.ok||r.type==="opaque"){{const cp=r.clone();caches.open(CACHE).then(c=>c.put(req,cp))}}return r}}).catch(()=>hit);return hit||net}}));
  }}
}});
'''
open(f"{OUT}/sw.js","w").write(sw)
print("built",ver)
