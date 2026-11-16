const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const mode = process.argv[2] || 'stills';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + __dirname + '/scene.html');
  await p.evaluate(async () => { await document.fonts.load('400 40px "Permanent Marker"'); await document.fonts.load('700 40px Kalam'); await document.fonts.load('400 40px "Patrick Hand"'); await document.fonts.ready; });
  const D = await p.evaluate(() => DURATION);
  fs.writeFileSync('timeline.json', JSON.stringify(await p.evaluate(() => timeline())));
  console.log('duration', D);
  const grab = async t => { await p.evaluate(t => renderAt(t), t); return Buffer.from((await p.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', .92))).split(',')[1], 'base64'); };
  if (mode === 'stills') {
    for (const t of process.argv.slice(3).map(Number)) fs.writeFileSync(`out/still_${t}.jpg`, await grab(t));
  } else {
    const fps = 30, n = Math.ceil(D * fps), active = [];
    const ff = spawn('ffmpeg', ['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','out/video_noaudio.mp4']);
    for (let i = 0; i < n; i++) {
      const t = i / fps;
      await p.evaluate(t => renderAt(t), t);
      active.push(await p.evaluate(t => renderAt(t), t) ? 1 : 0);
      const buf = Buffer.from((await p.evaluate(() => document.getElementById('c').toDataURL('image/jpeg', .93))).split(',')[1], 'base64');
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log('frame', i, '/', n);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    fs.writeFileSync('out/active.json', JSON.stringify({ fps, active }));
  }
  await b.close();
})();
