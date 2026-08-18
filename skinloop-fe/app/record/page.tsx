"use client";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { api, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";
import type { RecordCreateRequest } from "@/types/api";
const DRAFT = "skinloop:record-draft";
const initial: RecordCreateRequest = {
  recordedAt: new Date().toISOString().slice(0, 10),
  sleepHours: 7,
  lateSnack: false,
  stressLevel: 3,
  exerciseMin: 0,
  cosmeticChanged: false,
  skinRedness: 3,
  skinAcneCount: 2,
  skinOiliness: 3,
  memo: "",
};
export default function RecordPage() {
  const router = useRouter();
  const updateTotal = useSessionStore((s) => s.setRecordSummary);
  const [form, setForm] = useState(initial);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [photo, setPhoto] = useState("");
  useEffect(() => {
    const saved = localStorage.getItem(DRAFT);
    if (saved)
      try {
        setForm(JSON.parse(saved));
      } catch {}
  }, []);
  useEffect(
    () => () => {
      if (photo) URL.revokeObjectURL(photo);
    },
    [photo],
  );
  function number<K extends keyof RecordCreateRequest>(key: K, value: string) {
    setForm((v) => ({ ...v, [key]: Number(value) }));
  }
  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMessage("");
    try {
      const result = await api.createRecord(form);
      localStorage.removeItem(DRAFT);
      updateTotal(result.totalRecords);
      router.push(result.patternReady ? "/analyzing" : "/");
    } catch (error) {
      localStorage.setItem(DRAFT, JSON.stringify(form));
      setBusy(false);
      if (error instanceof ApiError && error.code === "DUPLICATE_DATE")
        setMessage(
          "이 날짜의 기록이 이미 있어요. 현재 백엔드에서는 수정 기능을 준비 중이에요.",
        );
      else
        setMessage(
          error instanceof ApiError
            ? `${error.message} 입력 내용은 임시 저장했어요.`
            : "저장하지 못했습니다. 입력 내용은 임시 저장했어요.",
        );
    }
  }
  return (
    <div className="page">
      <header className="page-header">
        <div>
          <h1 className="page-title">오늘의 기록</h1>
          <p className="subtle">
            생활 습관과 피부 상태를 약 1분 안에 남겨보세요.
          </p>
        </div>
      </header>
      <form className="stack" onSubmit={submit}>
        <section className="card stack">
          <h2 style={{ margin: 0, fontSize: 18 }}>생활 습관</h2>
          <label>
            <span className="label">날짜</span>
            <input
              className="field"
              type="date"
              required
              value={form.recordedAt}
              onChange={(e) => setForm({ ...form, recordedAt: e.target.value })}
            />
          </label>
          <label>
            <span className="label">수면 시간: {form.sleepHours}시간</span>
            <input
              className="field"
              type="range"
              min="0"
              max="14"
              step="0.5"
              value={form.sleepHours}
              onChange={(e) => number("sleepHours", e.target.value)}
            />
          </label>
          <div className="grid-2">
            <label className="card">
              <input
                type="checkbox"
                checked={form.lateSnack}
                onChange={(e) =>
                  setForm({ ...form, lateSnack: e.target.checked })
                }
              />{" "}
              야식을 먹었어요
            </label>
            <label className="card">
              <input
                type="checkbox"
                checked={form.cosmeticChanged}
                onChange={(e) =>
                  setForm({ ...form, cosmeticChanged: e.target.checked })
                }
              />{" "}
              화장품을 바꿨어요
            </label>
          </div>
          <label>
            <span className="label">스트레스: {form.stressLevel}/5</span>
            <input
              className="field"
              type="range"
              min="1"
              max="5"
              value={form.stressLevel}
              onChange={(e) => number("stressLevel", e.target.value)}
            />
          </label>
          <label>
            <span className="label">운동: {form.exerciseMin}분</span>
            <input
              className="field"
              type="range"
              min="0"
              max="120"
              step="10"
              value={form.exerciseMin}
              onChange={(e) => number("exerciseMin", e.target.value)}
            />
          </label>
        </section>
        <section className="card stack">
          <h2 style={{ margin: 0, fontSize: 18 }}>피부 상태</h2>
          {(
            [
              ["skinRedness", "붉은기"],
              ["skinAcneCount", "트러블 정도"],
              ["skinOiliness", "유분감"],
            ] as const
          ).map(([key, label]) => (
            <label key={key}>
              <span className="label">
                {label}: {form[key]}/5
              </span>
              <input
                className="field"
                type="range"
                min="1"
                max="5"
                value={form[key]}
                onChange={(e) => number(key, e.target.value)}
              />
            </label>
          ))}
          <label>
            <span className="label">메모 (선택)</span>
            <textarea
              className="field"
              maxLength={200}
              value={form.memo}
              onChange={(e) => setForm({ ...form, memo: e.target.value })}
            />
          </label>
          <label>
            <span className="label">
              피부 사진 (선택, 현재 기기에만 미리보기)
            </span>
            <input
              className="field"
              type="file"
              accept="image/*"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) setPhoto(URL.createObjectURL(f));
              }}
            />
          </label>
          {photo && (
            <Image
              unoptimized
              src={photo}
              alt="선택한 피부 사진 미리보기"
              width={180}
              height={180}
              style={{
                width: 180,
                height: 180,
                objectFit: "cover",
                borderRadius: 12,
              }}
            />
          )}
        </section>
        {message && (
          <p className="error-text" role="alert">
            {message}
          </p>
        )}
        <button className="btn btn-primary btn-block" disabled={busy}>
          {busy ? "저장하고 있어요…" : "기록 저장하기"}
        </button>
      </form>
    </div>
  );
}
