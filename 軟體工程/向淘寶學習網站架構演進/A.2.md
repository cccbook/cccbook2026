# A.2 Dockerfile 與 Compose 速查

本節只收錄本書用得到的指令（對應 Ch 7）。完整手冊請查官方文件，這裡求「考前 5 分鐘能背起來」。

## Dockerfile 常用指令

| 指令 | 用途 | 範例 |
|------|------|------|
| FROM | 基底映像 | `FROM openjdk:17-slim` |
| WORKDIR | 工作目錄 | `WORKDIR /app` |
| COPY | 複製檔案 | `COPY target/app.jar app.jar` |
| RUN | 建置期執行 | `RUN apt-get update && apt-get install -y curl` |
| EXPOSE | 聲明端口 | `EXPOSE 8080` |
| ENV | 環境變數 | `ENV SPRING_PROFILES_ACTIVE=prod` |
| CMD | 預設啟動命令 | `CMD ["java","-jar","app.jar"]` |
| ENTRYPOINT | 固定入口 | `ENTRYPOINT ["java","-jar","app.jar"]` |
| HEALTHCHECK | 健康檢查 | `HEALTHCHECK CMD curl -f http://localhost:8080/actuator/health` |

最小可用範本（Spring Boot）：

```dockerfile
FROM openjdk:17-slim
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```

```bash
# 建置、執行、驗證
docker build -t shop:v1 .
docker images | grep shop
docker run -d --name shop -p 8080:8080 shop:v1
docker ps && docker logs -f shop
curl http://localhost:8080/actuator/health
```

## Compose 欄位速查

| 欄位 | 用途 | 範例 |
|------|------|------|
| services | 定義服務 | `web: / db: / redis:` |
| image / build | 映像或建置路徑 | `image: nginx:1.25` / `build: ./web` |
| ports | 端口映射 | `"8080:8080"` |
| environment | 環境變數 | `SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/shop` |
| depends_on | 啟動順序 | `depends_on: [db, redis]` |
| volumes | 持久化 | `db-data:/var/lib/mysql` |
| networks | 自定網路 | `networks: [shopnet]` |
| restart | 重啟策略 | `restart: unless-stopped` |
| healthcheck | 健康檢查 | 見下例 |

本書標準四件套（Ch 7.4）：

```yaml
services:
  web:
    build: ./web
    ports: ["8080:8080"]
    depends_on: [db, redis]
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/shop
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes: [db-data:/var/lib/mysql]
  redis:
    image: redis:7
  nginx:
    image: nginx:1.25
    ports: ["80:80"]
volumes:
  db-data:
```

```bash
docker compose up -d --build
docker compose ps && docker compose logs -f
docker compose down && docker compose down -v   # 第二個會清 volume，慎用
```

## 排錯命令

```bash
docker logs --tail=100 shop          # 看啟動報錯
docker exec -it shop sh              # 進容器排查
docker inspect shop | grep -A5 Mounts
docker stats                         # 看誰吃光記憶體
docker system df && docker system prune -f
```

| 症狀 | 可能原因 | 解法 |
|------|---------|------|
| 端口衝突 | 8080 被佔用 | 改 ports 或停舊容器 |
| 連不上 db | 用了 localhost | 改用服務名 `db:3306` |
| 改碼沒生效 | 用到舊映像快取 | `up -d --build` |
| 磁碟爆了 | 殘留映像太多 | `system prune -f` |

## 本章小結

- Dockerfile 背：FROM → WORKDIR → COPY → RUN → EXPOSE → CMD。
- Compose 背：services / ports / environment / depends_on / volumes。
- 排錯三招：`logs` 看錯、`exec` 進去、`ps + stats` 看狀態。

## 練一練

1. 為一個靜態頁寫 Dockerfile（`nginx:1.25` + COPY），build 並用瀏覽器打開驗證。
2. 用上面四件套啟動一次，故意把 `db` 主機寫錯，觀察 `logs` 報錯再修好。
3. 不清 volume 與清 volume 各做一次 `down`，比較重啟後 MySQL 資料是否還在。
