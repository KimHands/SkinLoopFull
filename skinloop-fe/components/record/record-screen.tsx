"use client";

import Image from "next/image";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";
import type { RecordCreateRequest } from "@/types/api";
import { ScaleSelector } from "./scale-selector";
import { ToggleRow } from "./toggle-row";

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

export default function RecordScreen() {
  const router = useRouter();
  const updateTotal = useSessionStore((state) => state.setRecordSummary);
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
  function setNumber(key: keyof RecordCreateRequest, value: number) {
    setForm((current) => ({ ...current, [key]: value }));
  }
  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    try {
      const result = await api.createRecord(form);
      localStorage.removeItem(DRAFT);
      updateTotal(result.totalRecords);
      router.push(result.patternReady ? "/analyzing" : "/");
    } catch (caught) {
      localStorage.setItem(DRAFT, JSON.stringify(form));
      setBusy(false);
      setMessage(
        caught instanceof ApiError
          ? `${caught.message} 입력 내용은 임시 저장했어요.`
          : "저장하지 못했어요. 입력 내용은 임시 저장했어요.",
      );
    }
  }

  return (
    <div className="page record-page">
      <header className="page-header">
        <div>
          <h1 className="page-title">오늘의 기록</h1>
          <p className="subtle">생활 습관과 피부 상태를 함께 남겨주세요.</p>
        </div>
      </header>
      <form className="stack" onSubmit={submit}>
        <section className="card stack">
          <h2 className="section-title">생활 습관</h2>
          <label>
            <span className="label">날짜</span>
            <input
              className="field"
              type="date"
              required
              value={form.recordedAt}
              onChange={(event) =>
                setForm({ ...form, recordedAt: event.target.value })
              }
            />
          </label>
          <label>
            <span className="scale-label">
              <strong>수면 시간</strong>
              <span>{form.sleepHours}시간</span>
            </span>
            <input
              className="range-field"
              type="range"
              min="0"
              max="14"
              step="0.5"
              value={form.sleepHours}
              onChange={(event) =>
                setNumber("sleepHours", Number(event.target.value))
              }
            />
          </label>
          <ToggleRow
            label="야식을 먹었어요"
            checked={form.lateSnack}
            onChange={(checked) => setForm({ ...form, lateSnack: checked })}
          />
          <ScaleSelector
            label="스트레스"
            value={form.stressLevel}
            onChange={(value) => setNumber("stressLevel", value)}
          />
          <label>
            <span className="scale-label">
              <strong>운동</strong>
              <span>{form.exerciseMin}분</span>
            </span>
            <input
              className="range-field"
              type="range"
              min="0"
              max="120"
              step="10"
              value={form.exerciseMin}
              onChange={(event) =>
                setNumber("exerciseMin", Number(event.target.value))
              }
            />
          </label>
          <ToggleRow
            label="화장품 변화"
            checked={form.cosmeticChanged}
            onChange={(checked) =>
              setForm({ ...form, cosmeticChanged: checked })
            }
          />
        </section>
        <section className="card stack">
          <h2 className="section-title">피부 상태</h2>
          <ScaleSelector
            label="붉은기"
            value={form.skinRedness}
            onChange={(value) => setNumber("skinRedness", value)}
          />
          <ScaleSelector
            label="트러블 개수"
            value={form.skinAcneCount}
            onChange={(value) => setNumber("skinAcneCount", value)}
          />
          <ScaleSelector
            label="유분감"
            value={form.skinOiliness}
            onChange={(value) => setNumber("skinOiliness", value)}
          />
        </section>
        <section className="card stack">
          <h2 className="section-title">사진 선택</h2>
          <label className="photo-upload">
            <input
              type="file"
              accept="image/*"
              onChange={(event) => {
                const file = event.target.files?.[0];
                if (file) setPhoto(URL.createObjectURL(file));
              }}
            />
            {photo ? (
              <Image
                unoptimized
                src={photo}
                alt="선택한 피부 사진 미리보기"
                width={220}
                height={150}
              />
            ) : (
              <>
                <b>＋</b>
                <span>오늘 피부 사진 추가</span>
              </>
            )}
          </label>
          <label>
            <span className="label">메모 (선택)</span>
            <textarea
              className="field"
              maxLength={200}
              value={form.memo}
              onChange={(event) =>
                setForm({ ...form, memo: event.target.value })
              }
            />
          </label>
        </section>
        {message && (
          <p className="error-text" role="alert">
            {message}
          </p>
        )}
        <button
          className="btn btn-primary btn-block sticky-action"
          disabled={busy}
        >
          {busy ? "저장하고 있어요…" : "저장"}
        </button>
      </form>
    </div>
  );
}
