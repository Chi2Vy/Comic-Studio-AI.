import { useEffect, useState, type FormEvent } from 'react';
import './SourceStudio.css';

type Source = { id: string; filename: string; format: string; character_count: number; segment_count: number };
type Segment = { segment_index: number; heading: string; char_count: number; preview: string };
type SourceDetail = Source & { preview: string; segments: Segment[] };
type SegmentDetail = Segment & { content: string };
type Props = { projectId: string; rightsStatus: string };

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(await errorMessage(response));
  return await response.json() as T;
}
async function errorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json() as { detail?: unknown };
    return typeof data.detail === 'string' ? data.detail : 'HTTP ' + response.status;
  } catch { return 'HTTP ' + response.status; }
}

export default function SourceStudio({ projectId, rightsStatus }: Props) {
  const base = '/api/projects/' + encodeURIComponent(projectId) + '/sources';
  const [sources, setSources] = useState<Source[]>([]);
  const [selected, setSelected] = useState('');
  const [detail, setDetail] = useState<SourceDetail | null>(null);
  const [segment, setSegment] = useState<SegmentDetail | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  useEffect(() => {
    let live = true;
    setSources([]); setSelected(''); setDetail(null); setSegment(null);
    setError(''); setNotice(''); setFile(null); setConfirmed(false);
    void getJson<Source[]>(base).then(data => { if (live) setSources(data); })
      .catch(e => { if (live) setError(String(e)); });
    return () => { live = false; };
  }, [base]);

  useEffect(() => {
    let live = true;
    setDetail(null); setSegment(null);
    if (selected) {
      void getJson<SourceDetail>(base + '/' + encodeURIComponent(selected))
        .then(data => { if (live) setDetail(data); })
        .catch(e => { if (live) setError(String(e)); });
    }
    return () => { live = false; };
  }, [base, selected]);

  async function upload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file || !confirmed || rightsStatus === 'unknown') return;
    const form = event.currentTarget;
    const data = new FormData();
    data.append('file', file); data.append('confirm_rights', 'true');
    setBusy(true); setError(''); setNotice('');
    try {
      const response = await fetch(base, { method: 'POST', body: data });
      if (!response.ok) throw new Error(await errorMessage(response));
      const added = await response.json() as Source;
      setSources(old => [added, ...old]); setSelected(added.id);
      setFile(null); setConfirmed(false); form.reset();
      setNotice('Đã nhập bản thảo và lưu riêng trong SQLite local.');
    } catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    finally { setBusy(false); }
  }

  async function readSegment(index: number) {
    if (!selected) return;
    setBusy(true); setError('');
    try {
      setSegment(await getJson<SegmentDetail>(base + '/' + encodeURIComponent(selected) + '/segments/' + index));
    } catch (e) { setError(String(e)); }
    finally { setBusy(false); }
  }

  return <section className="source-studio">
    <div className="source-head">
      <div><small className="source-kicker">NGHIÊN CỨU NGUYÊN TÁC · PHASE 2</small>
      <h2>Kho bản thảo nguồn</h2>
      <p>Nhập tệp, đọc nội dung và nhận diện tiêu đề chương. Chưa tự tạo kịch bản hay xác minh nguyên tác bằng AI.</p></div>
      <span className="source-local">● Chỉ lưu local</span>
    </div>
    <div className="source-layout">
      <div className="source-sidebar">
        <h3>Bản thảo ({sources.length})</h3>
        {sources.length===0 && <p className="source-muted">Chưa có tệp. Nhập bản thảo có quyền sử dụng để bắt đầu.</p>}
        {sources.map(doc => <button type="button" key={doc.id} className={'source-item '+(selected===doc.id?'active':'')} onClick={() => setSelected(doc.id)}>
          <strong>{doc.filename}</strong>
          <small>{doc.format.toUpperCase()} · {doc.segment_count} phần · {doc.character_count.toLocaleString('vi-VN')} ký tự</small>
        </button>)}
        <form className="source-upload" onSubmit={e=>void upload(e)}>
          <h3>Thêm bản thảo</h3>
          <label htmlFor="source-file">Chọn TXT, DOCX, EPUB hoặc PDF (tối đa 8 MB)</label>
          <input id="source-file" type="file" accept=".txt,.docx,.epub,.pdf" onChange={e=>setFile(e.target.files?.[0]||null)}/>
          <label className="source-confirm">
            <input type="checkbox" checked={confirmed} onChange={e=>setConfirmed(e.target.checked)}/>
            <span>Tôi có quyền sử dụng tài liệu này trong studio.</span>
          </label>
          {rightsStatus==='unknown' && <p className="source-warning">Chưa xác nhận quyền nguồn cho dự án. Cần tạo dự án với trạng thái quyền phù hợp.</p>}
          <button className="source-submit" disabled={!file||!confirmed||busy||rightsStatus==='unknown'}>{busy?'Đang xử lý…':'Nhập bản thảo'}</button>
          <p className="source-muted">Văn bản được lưu ở cơ sở dữ liệu local. PDF scan chưa có OCR, tệp không được gửi lên GPT.</p>
        </form>
      </div>
      <div className="source-reader">
        {!detail ? <p className="source-empty">Chọn một bản thảo để xem các phần/chương nhận diện được.</p> : <>
          <h3>{detail.filename}</h3>
          <p className="source-muted">{detail.character_count.toLocaleString('vi-VN')} ký tự · {detail.segment_count} phần</p>
          <div className="source-chapters">
            <h4>Chương / phần</h4>
            {detail.segments.map(s => <button className={'source-chapter '+(segment?.segment_index===s.segment_index?'active':'')} type="button" key={s.segment_index} onClick={()=>void readSegment(s.segment_index)}>
              <span>{s.segment_index}. {s.heading}</span><small>{s.char_count.toLocaleString('vi-VN')} ký tự</small>
            </button>)}
          </div>
          <div className="source-preview">
            <h4>{segment?.heading||'Xem trước 5.000 ký tự đầu'}</h4>
            <pre>{segment?.content||detail.preview}</pre>
          </div>
          <p className="source-muted">Đây mới là phân đoạn tự động theo tiêu đề, chưa phải chương đã kiểm chứng. Beat Ledger bên dưới do người dùng nhập.</p>
        </>}
      </div>
    </div>
    {error && <div role="alert" className="source-error">{error}</div>}
    {notice && <div role="status" className="source-ok">{notice}</div>}
  </section>;
}
