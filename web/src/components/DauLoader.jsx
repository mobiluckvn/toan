import React, { useEffect, useState } from 'react';
import { CONTENT, dongDau } from '../lib/content.js';
import DauPlayer from './DauPlayer.jsx';

/** Nạp một khối Quyển 2 rồi trao cho DauPlayer — tách ra cho App gọn */
export default function DauLoader({ khoiId, onExit, onXong, onMoMicro }) {
  const [khoi, setKhoi] = useState(null);
  const [loi, setLoi] = useState(null);

  useEffect(() => {
    const ten = khoiId.replace('DR:', 'DR_').replace(/\./g, '_');
    fetch(dongDau(`${CONTENT}/quyen2/${ten}.json`))
      .then((r) => { if (!r.ok) throw new Error(`không nạp được ${ten}`); return r.json(); })
      .then(setKhoi)
      .catch((e) => setLoi(String(e?.message || e)));
  }, [khoiId]);

  if (loi) return <div className="p-6 text-alert">{loi}</div>;
  if (!khoi) return <div className="p-6 text-mute">Đang mở vòng đấu…</div>;
  return <DauPlayer khoi={khoi} onExit={onExit} onXong={onXong} onMoMicro={onMoMicro} />;
}
