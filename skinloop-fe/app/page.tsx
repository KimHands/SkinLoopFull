"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { api,ApiError } from "@/lib/api-client";
import { useSessionStore } from "@/stores/session-store";

export default function HomePage(){
 const router=useRouter(); const total=useSessionStore(s=>s.totalRecords); const isDemo=useSessionStore(s=>s.isDemo); const setDemo=useSessionStore(s=>s.setDemoMode); const [busy,setBusy]=useState(false); const [error,setError]=useState(""); const need=Math.max(0,7-total);
 async function loadDemo(){setBusy(true);setError("");try{const result=await api.loadDemo();setDemo(true,result.recordDays);router.push("/analyzing")}catch(e){setError(e instanceof ApiError?e.message:"샘플을 불러오지 못했습니다.");setBusy(false)}}
 return <div className="page stack">
  <header className="page-header"><div><div style={{color:"var(--primary-dark)",fontWeight:800,fontSize:24}}>SkinLoop</div><p className="subtle" style={{margin:"6px 0 0"}}>오늘의 생활과 피부 변화를 함께 기록해요.</p></div></header>
  <section className="grid-2">
   <div className="card home-summary-card"><p className="caption">오늘의 체크인</p><h1 className="page-title">{total?`${total}일째 기록 중`:"첫 기록을 시작해 볼까요?"}</h1><p className="subtle">작은 기록이 쌓이면 반복적으로 함께 나타나는 패턴을 살펴볼 수 있어요.</p><Link className="btn btn-primary btn-block" href="/record">오늘 기록하기</Link></div>
   <div className="card home-summary-card"><p className="caption">분석 진행도</p>{total<7?<><h2 style={{fontSize:18}}>앞으로 {need}일 더 기록하면 분석이 시작돼요</h2><div style={{height:10,borderRadius:9,background:"var(--border)",overflow:"hidden",margin:"8px 0 0"}}><div style={{width:`${Math.min(total/7*100,100)}%`,height:"100%",background:"var(--primary)"}}/></div><p className="caption">{total}일 기록 / 7일</p></>:<><h2 style={{fontSize:18}}>새 인사이트를 확인할 수 있어요</h2><p className="subtle">최근 기록을 기준으로 연관 가능성이 높은 생활 습관을 살펴보세요.</p><Link className="btn btn-secondary btn-block" href="/analyzing">인사이트 보기</Link></>}</div>
  </section>
  {!isDemo&&<section className="card"><h2 style={{marginTop:0,fontSize:18}}>28일치 샘플로 먼저 둘러보기</h2><p className="subtle">기록을 기다리지 않고 인사이트와 4주 시나리오를 체험할 수 있어요. 현재 기록은 샘플로 교체됩니다.</p><button className="btn btn-outline btn-block" disabled={busy} onClick={()=>void loadDemo()}>{busy?"샘플을 준비하고 있어요…":"샘플 데이터로 체험하기"}</button>{error&&<p className="error-text" role="alert">{error}</p>}</section>}
 </div>
}
