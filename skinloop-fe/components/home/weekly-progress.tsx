const days = ["월", "화", "수", "목", "금", "토", "일"];

export function WeeklyProgress({ filled }: { filled: number }) {
  return (
    <div className="week-row">
      {days.map((day, index) => (
        <div className="week-day" key={day}>
          <span>{day}</span>
          <i className={index < filled ? "filled" : ""} />
        </div>
      ))}
    </div>
  );
}
