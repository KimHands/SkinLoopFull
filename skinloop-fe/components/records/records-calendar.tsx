import type { RecordItem } from "@/types/api";

export function RecordsCalendar({ records }: { records: RecordItem[] }) {
  const latest = records.at(-1)?.recordedAt;
  const base = latest ? new Date(`${latest}T00:00:00`) : new Date();
  const year = base.getFullYear();
  const month = base.getMonth();
  const last = new Date(year, month + 1, 0).getDate();
  const offset = (new Date(year, month, 1).getDay() + 6) % 7;
  const recorded = new Set(
    records
      .filter((item) => {
        const date = new Date(`${item.recordedAt}T00:00:00`);
        return date.getFullYear() === year && date.getMonth() === month;
      })
      .map((item) => new Date(`${item.recordedAt}T00:00:00`).getDate()),
  );
  return (
    <section className="card calendar-card">
      <div className="calendar-heading">
        <strong>
          {year}년 {month + 1}월
        </strong>
        <div>
          <button aria-label="이전 달">‹</button>
          <button aria-label="다음 달">›</button>
        </div>
      </div>
      <div className="calendar-grid calendar-week">
        {["일", "월", "화", "수", "목", "금", "토"].map((day) => (
          <span key={day}>{day}</span>
        ))}
      </div>
      <div className="calendar-grid calendar-days">
        {Array.from({ length: offset }, (_, index) => (
          <i key={`blank-${index}`} />
        ))}
        {Array.from({ length: last }, (_, index) => {
          const day = index + 1;
          return (
            <span key={day} className={recorded.has(day) ? "recorded" : ""}>
              {day}
            </span>
          );
        })}
      </div>
      <div className="calendar-key">
        <span>● 기록 있음</span>
        <span>○ 기록 없음</span>
      </div>
    </section>
  );
}
