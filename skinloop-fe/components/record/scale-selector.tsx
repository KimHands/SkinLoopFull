export function ScaleSelector({
  label,
  value,
  onChange,
}: {
  label: string;
  value: number;
  onChange: (value: number) => void;
}) {
  return (
    <div className="scale-field">
      <div className="scale-label">
        <strong>{label}</strong>
        <span>{value}/5</span>
      </div>
      <div className="scale-options">
        {[1, 2, 3, 4, 5].map((item) => (
          <button
            type="button"
            className={value === item ? "selected" : ""}
            key={item}
            onClick={() => onChange(item)}
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}
