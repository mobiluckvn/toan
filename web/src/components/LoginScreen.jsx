import React, { useEffect, useRef, useState } from 'react';
import { requestOtp, verifyOtp, loginAdmin } from '../lib/firebase.js';

const CODE_LEN = 6;
const RESEND_S = 60;

/**
 * Lỗi từ máy chủ về dạng mã kỹ thuật — dịch sang câu bố mẹ đọc hiểu.
 *
 * Quan trọng: KHÔNG bao giờ để lọt mã trần ra màn hình. Firebase trả về những chuỗi như
 * "internal", "unavailable", "functions/not-found" — bố mẹ nhìn vào không hiểu gì mà
 * cũng chẳng biết phải làm sao. Cái gì không nhận ra thì nói một câu tử tế chung.
 */
export function niceError(e) {
  const raw = String(e?.message || e || '').replace(/^Firebase:\s*/, '');
  const low = raw.toLowerCase();

  // Thông điệp mình tự viết ở máy chủ đã là tiếng Việt — giữ nguyên, bỏ tiền tố mã lỗi.
  // Không phải tiếng Việt thì đó là lỗi hệ thống, KHÔNG hiện trần cho bố mẹ xem.
  if (low.includes('resource-exhausted') || low.includes('permission-denied')) {
    const vi = raw.replace(/^.*?:\s*/, '').trim();
    if (/[àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềể]/i.test(vi)) return vi;
    return low.includes('resource-exhausted')
      ? 'Bạn thao tác hơi nhanh. Chờ một lát rồi thử lại nhé.'
      : 'Mã không đúng hoặc đã hết hạn. Bạn xin mã mới nhé.';
  }
  if (low.includes('invalid-argument')) return 'Email chưa đúng. Bạn kiểm tra lại giúp nhé.';
  if (low.includes('wrong-password') || low.includes('invalid-credential')
      || low.includes('user-not-found')) return 'Email hoặc mật khẩu chưa đúng.';
  if (low.includes('too-many-requests')) return 'Thử quá nhiều lần rồi. Nghỉ một lát rồi thử lại nhé.';
  if (low.includes('unavailable') || low.includes('network') || low.includes('deadline'))
    return 'Mạng đang chập chờn. Bạn thử lại giúp nhé.';
  if (low.includes('internal') || low.includes('not-found') || low.includes('unauthenticated'))
    return 'Chưa gọi được máy chủ. Bạn thử lại sau ít phút, hoặc bấm "Để sau" để cho con học trước nhé.';

  // Còn lại: CHỈ hiện khi chắc chắn là câu tiếng Việt mình tự viết.
  // Cứ còn dấu vết mã lỗi hoặc không có dấu tiếng Việt thì nuốt đi.
  const hasVietnamese = /[àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềể]/i.test(raw);
  const hasCode = /[a-z]+-[a-z]+|[a-z]+\/[a-z-]+|firebaseerror/i.test(raw);
  return hasVietnamese && !hasCode ? raw : 'Có trục trặc nhỏ. Bạn thử lại giúp nhé.';
}

/**
 * ĐĂNG NHẬP — hai bước: nhập email, rồi nhập mã 6 số nhận qua thư.
 * Không có màn đăng ký: chưa có tài khoản thì hệ thống lập luôn khi nhập đúng mã.
 */
export default function LoginScreen({ onDone, onSkip }) {
  const [step, setStep] = useState('email');       // email · code · admin
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [note, setNote] = useState('');
  const [left, setLeft] = useState(0);             // giây còn lại trước khi cho gửi lại
  const [pw, setPw] = useState('');
  const codeRef = useRef(null);

  useEffect(() => {
    if (left <= 0) return undefined;
    const id = setTimeout(() => setLeft((n) => n - 1), 1000);
    return () => clearTimeout(id);
  }, [left]);

  useEffect(() => { if (step === 'code') codeRef.current?.focus(); }, [step]);

  const send = async (again = false) => {
    setErr(''); setBusy(true);
    try {
      const r = await requestOtp(email);
      setNote(r?.message || 'Đã gửi mã. Bạn kiểm tra hộp thư nhé.');
      setStep('code'); setLeft(RESEND_S);
      if (again) setCode('');
    } catch (e) { setErr(niceError(e)); }
    finally { setBusy(false); }
  };

  const check = async () => {
    setErr(''); setBusy(true);
    try { onDone(await verifyOtp(email, code)); }
    catch (e) { setErr(niceError(e)); setCode(''); codeRef.current?.focus(); }
    finally { setBusy(false); }
  };

  const asAdmin = async () => {
    setErr(''); setBusy(true);
    try { await loginAdmin(email, pw); onDone({ role: 'admin' }); }
    catch (e) { setErr(niceError(e)); }
    finally { setBusy(false); }
  };

  return (
    <div className="mx-auto flex min-h-[100dvh] max-w-[440px] flex-col justify-center px-4 py-8">
      <div className="mb-5 text-center">
        <div className="text-[11px] font-extrabold tracking-widest text-gold-dark">MOBILUCK · KỸ SƯ NHÍ</div>
        <h1 className="mt-1 text-[22px] font-bold text-navy">Toán Tư Duy lớp 5</h1>
      </div>

      <div className="card">
        {step === 'email' && (
          <>
            <h2 className="text-[17px] font-bold text-navy">Đăng nhập</h2>
            <p className="mt-1 text-[14px] leading-relaxed text-mute">
              Nhập email, chúng tôi gửi bạn một mã 6 số. Chưa có tài khoản thì hệ thống
              tự lập giúp — không cần đăng ký riêng.
            </p>
            <label className="field mt-3.5 block">
              <span className="field-head">Email của bố mẹ</span>
              <input className="numin w-full text-[16px]" type="email" inputMode="email"
                     autoComplete="email" placeholder="vidu@gmail.com" value={email}
                     onChange={(e) => setEmail(e.target.value)}
                     onKeyDown={(e) => e.key === 'Enter' && email && !busy && send()} />
            </label>
            <button className="btn-go mt-3.5" disabled={!email || busy} onClick={() => send()}>
              {busy ? 'Đang gửi…' : 'Gửi mã cho tôi'}
            </button>
          </>
        )}

        {step === 'code' && (
          <>
            <h2 className="text-[17px] font-bold text-navy">Nhập mã trong thư</h2>
            <p className="mt-1 text-[14px] leading-relaxed text-mute">
              Đã gửi tới <b className="text-navy">{email}</b>. Mã có hiệu lực 10 phút.
              Không thấy thư thì xem cả mục spam nhé.
            </p>
            <input ref={codeRef} className="numin mt-3.5 w-full text-center text-[26px] tracking-[.4em]"
                   inputMode="numeric" autoComplete="one-time-code" placeholder="••••••"
                   value={code}
                   onChange={(e) => {
                     // dán cả dòng "Mã: 123456" vẫn nhặt đúng 6 chữ số
                     const digits = e.target.value.replace(/\D/g, '').slice(0, CODE_LEN);
                     setCode(digits);
                     if (digits.length === CODE_LEN) setErr('');
                   }}
                   onKeyDown={(e) => e.key === 'Enter' && code.length === CODE_LEN && !busy && check()} />
            <button className="btn-go mt-3.5" disabled={code.length !== CODE_LEN || busy} onClick={check}>
              {busy ? 'Đang kiểm…' : 'Vào học'}
            </button>
            <div className="mt-3 flex items-center justify-between text-[13px]">
              <button className="font-semibold text-navy underline"
                      onClick={() => { setStep('email'); setErr(''); setCode(''); }}>
                Đổi email
              </button>
              <button className="font-semibold text-navy disabled:text-mute disabled:no-underline underline"
                      disabled={left > 0 || busy} onClick={() => send(true)}>
                {left > 0 ? `Gửi lại sau ${left}s` : 'Gửi lại mã'}
              </button>
            </div>
          </>
        )}

        {step === 'admin' && (
          <>
            <h2 className="text-[17px] font-bold text-navy">Quản trị hệ thống</h2>
            <p className="mt-1 text-[14px] text-mute">Tài khoản quản trị vào bằng mật khẩu.</p>
            <label className="field mt-3.5 block">
              <span className="field-head">Email</span>
              <input className="numin w-full text-[16px]" type="email" value={email}
                     onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label className="field mt-2.5 block">
              <span className="field-head">Mật khẩu</span>
              <input className="numin w-full text-[16px]" type="password" value={pw}
                     autoComplete="current-password"
                     onChange={(e) => setPw(e.target.value)}
                     onKeyDown={(e) => e.key === 'Enter' && !busy && asAdmin()} />
            </label>
            <button className="btn-go mt-3.5" disabled={!email || !pw || busy} onClick={asAdmin}>
              {busy ? 'Đang vào…' : 'Đăng nhập'}
            </button>
          </>
        )}

        {err && (
          <p className="mt-3 rounded-xl border-[1.5px] border-alert bg-alert-pale px-3 py-2.5 text-[14px] text-alert">
            {err}
          </p>
        )}
        {!err && note && step === 'code' && (
          <p className="mt-3 rounded-xl bg-teal-pale px-3 py-2.5 text-[13.5px] text-teal-dark">{note}</p>
        )}
      </div>

      <button className="mt-2 text-center text-[13.5px] font-semibold text-navy underline" onClick={onSkip}>
        Để sau — cho con học thử trước
      </button>
      <p className="mt-1 px-2 text-center text-[12px] leading-relaxed text-mute">
        Học thử vẫn lưu bài tại máy. Đăng nhập lúc nào thì toàn bộ kết quả được đẩy lên, không mất gì.
      </p>

      <button className="mt-5 text-center text-[12px] text-mute underline"
              onClick={() => { setStep(step === 'admin' ? 'email' : 'admin'); setErr(''); }}>
        {step === 'admin' ? '← Quay lại đăng nhập thường' : 'Tôi là quản trị hệ thống'}
      </button>
    </div>
  );
}
