import type { WhatIfResponse } from "@/types/api";

export function TrendChart({ data }: { data: WhatIfResponse }) {
  const values = [
    ...data.current.trend,
    ...data.changed.trend,
    data.current.range.min,
    data.current.range.max,
    data.changed.range.min,
    data.changed.range.max,
  ];
  const min = Math.floor(Math.min(...values) / 10) * 10 - 5;
  const max = Math.ceil(Math.max(...values) / 10) * 10 + 5;
  const y = (value: number) =>
    130 - ((value - min) / Math.max(max - min, 1)) * 95;
  const points = (trend: number[]) =>
    trend.map((value, index) => `${20 + index * 82},${y(value)}`).join(" ");
  const band = (range: { min: number; max: number }, fill: string) => (
    <rect
      x="20"
      width="246"
      y={y(range.max)}
      height={Math.max(y(range.min) - y(range.max), 2)}
      rx="5"
      fill={fill}
    />
  );
  return (
    <svg
      viewBox="0 0 286 165"
      role="img"
      aria-label="현재 유지와 습관 변경 시 4주 예상 흐름 비교"
    >
      {[35, 70, 105, 140].map((line) => (
        <line
          key={line}
          x1="20"
          x2="266"
          y1={line}
          y2={line}
          stroke="#eee6e2"
        />
      ))}
      {band(data.current.range, "rgba(157,145,139,.13)")}
      {band(data.changed.range, "rgba(139,111,158,.14)")}
      <polyline
        points={points(data.current.trend)}
        fill="none"
        stroke="#aaa09b"
        strokeWidth="2.5"
        strokeDasharray="5 4"
      />
      <polyline
        points={points(data.changed.trend)}
        fill="none"
        stroke="#8a6d9e"
        strokeWidth="2.5"
      />
      {["1주", "2주", "3주", "4주"].map((label, index) => (
        <text
          key={label}
          x={15 + index * 82}
          y="160"
          fontSize="10"
          fill="#89858a"
        >
          {label}
        </text>
      ))}
    </svg>
  );
}
