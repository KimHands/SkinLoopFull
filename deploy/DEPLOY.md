# 가비아 서버 배포 런북

멋사 가비아 클라우드 서버 1대(2vCore/4GB, 공인 IP 1개)에 nginx + FE + BE + PostgreSQL을
docker compose로 올린다. ⚠️ **서버는 2026-08-28 23:59 일괄 삭제** → 데이터/코드 백업 필수.

## 0. 준비물
- 공인 IP, SSH 접속(계정 + 키), (선택) 도메인, (선택) OPENAI_API_KEY.

## 1. 서버 초기 세팅 (root/sudo)
```bash
# 패키지 최신화 + Docker
sudo apt-get update && sudo apt-get -y upgrade
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"   # 재로그인 후 sudo 없이 docker

# swap 2G (4GB 메모리 빌드 여유)
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 방화벽: SSH + HTTP(+HTTPS)
sudo ufw allow OpenSSH && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw --force enable
```
> 가비아 콘솔의 보안그룹/방화벽에서도 22/80/443 인바운드 허용 필요.

## 2. 레포 배치 + 운영 .env
```bash
git clone https://github.com/KimHands/skinloop-full.git
cd skinloop-full
cp .env.example .env
```
`.env` 운영값(예):
```
POSTGRES_PASSWORD=<강한-비밀번호>
CORS_ORIGINS=http://<공인IP-또는-도메인>
OPENAI_API_KEY=            # 비워도 규칙기반 폴백으로 동작. 나중에 채워도 됨.
NEXT_PUBLIC_API_BASE=http://<공인IP-또는-도메인>
```
> ⚠️ `NEXT_PUBLIC_API_BASE`는 **FE 빌드 시점에 인라인**된다. 값을 바꾸면 반드시 FE 재빌드
> (`docker compose build fe` 후 `up -d`). `.env`는 커밋 금지(gitignore됨).

## 3. 기동 + 스키마 초기화
```bash
bash deploy/deploy.sh
```
- `docker compose up -d --build` 로 4개 서비스 기동.
- 테이블은 BE가 `AUTO_INIT_DB=1`(compose 설정)로 시작 시 자동 생성.
- 프로덕션에서 자동생성을 끄려면 compose의 `AUTO_INIT_DB`를 지우고 스키마를 수동 생성.

## 4. 스모크 (제출 요건 F-01 / NF-01~03)
```bash
bash deploy/smoke.sh http://<공인IP-또는-도메인>
```
- 세션(로그인 없이 진입) → 데모 28일 → 패턴/시나리오 실제 렌더 → 실험 → FE 홈.
- 브라우저로 `http://<공인IP-또는-도메인>` 접속: 로그인 없이 3초 내 진입(F-01),
  다른 기기/브라우저에서도 접속 확인(NF-01~03).

## 5. 제출 요건 마감
- GitHub `main` 최신·**Public** (이미 충족), 코드=배포 일치(배포는 main 빌드).
- 배포 URL을 행사 종료까지 상시 접속 유지.
- 서버 삭제(8/28) 전 DB 백업: `docker compose exec db pg_dump -U skinloop skinloop > backup.sql`.

## (선택) HTTPS
도메인이 있으면 nginx 컨테이너 대신 호스트 nginx + certbot, 또는 caddy로 TLS 종단.
행사용 데모는 http로도 충분.

## 롤백/운영
```bash
docker compose ps            # 상태
docker compose logs -f be    # 로그
docker compose down          # 중지(볼륨 유지)
docker compose up -d --build # 재기동
```
