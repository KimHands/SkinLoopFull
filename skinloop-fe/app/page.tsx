import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 py-10 text-center">
      <h1 className="text-2xl font-bold">SkinLoop</h1>
      <p className="text-sm text-gray-500">오늘의 피부, 기록해 볼까요?</p>
      <div className="flex flex-col gap-3">
        <Link href="/record" className="rounded-lg bg-black px-6 py-3 text-white">
          오늘 기록하기
        </Link>
        <span className="text-xs text-gray-400">— 또는 —</span>
        <button className="rounded-lg border px-6 py-3">28일치 샘플로 둘러보기</button>
      </div>
    </main>
  );
}
