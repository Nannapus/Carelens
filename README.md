#  Relax Activity Suggestion App

แอปพลิเคชันแนะนำกิจกรรมพักผ่อนคลายเครียดเป็นภาษาไทย ที่พัฒนาด้วย Flask และ Docker

##  คำอธิบายโปรเจค

โปรเจคนี้เป็นระบบ Microservices ที่ประกอบด้วย 2 บริการหลัก:

- **Container 1 (Main Service)** - API หลักที่รับคำขอจากผู้ใช้และส่งข้อความพักผ่อน
- **Container 2 (Activity Service)** - บริการแนะนำกิจกรรมพักผ่อนแบบสุ่มจากรายการ 49 กิจกรรม

##  สถาปัตยกรรม

```
User Request → Container 1 (Port 5000) → Container 2 (Port 5001)
                     ↓
            Return relaxation message + activity
```

### การทำงานของระบบ:
1. ผู้ใช้เรียก API `/relax` ที่ Container 1
2. Container 1 ส่งคำขอไปยัง Container 2 เพื่อขอกิจกรรมสุ่ม
3. Container 2 สุ่มเลือกกิจกรรมและส่งกลับ
4. Container 1 รวมข้อความและส่งผลลัพธ์กลับให้ผู้ใช้

##  โครงสร้างไฟล์

```
relax-app/
├── container1/
│   ├── app.py
│   └── Dockerfile
├── container2/
│   ├── app.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

##  วิธีการ Deploy

### ข้อกำหนดเบื้องต้น
- Docker
- Docker Compose

### ขั้นตอนการติดตั้ง

1. **Clone โปรเจค**
```bash
git clone https://github.com/Nannapus/Carelens.git
cd relax-app
```

2. **สร้างและรันคอนเทนเนอร์**
```bash
docker-compose up --build
```

3. **รันในโหมด Background (ไม่บังคับ)**
```bash
docker-compose up -d --build
```

4. **ตรวจสอบสถานะคอนเทนเนอร์**
```bash
docker-compose ps
```

##  วิธีการทดสอบระบบ

### 1. ทดสอบ API หลัก (Container 1)

**ผ่าน cURL:**
```bash
curl http://localhost:5000/relax
```

**ผ่าน Browser:**
เปิดเบราว์เซอร์ไปที่ `http://localhost:5000/relax`

**ตัวอย่างผลลัพธ์:**
```json
{
  "message": "ถึงเวลาคลายเครียดแล้ว!",
  "suggested_activity": "เดินเล่นรอบบ้าน"
}
```

### 2. ทดสอบ Activity Service (Container 2)

**ผ่าน cURL:**
```bash
curl http://localhost:5001/activity
```

**ตัวอย่างผลลัพธ์:**
```json
{
  "activity": "ทำสมาธิ 10 นาที"
}
```

### 3. ทดสอบการเชื่อมต่อระหว่างคอนเทนเนอร์

รันคำสั่งนี้หลายครั้งเพื่อดูว่ากิจกรรมเปลี่ยนแปลงแบบสุ่มหรือไม่:
```bash
for i in {1..5}; do curl http://localhost:5000/relax; echo; done
```

##  คำสั่งที่มีประโยชน์

### ดู Logs
```bash
# ดู logs ทั้งหมด
docker-compose logs

# ดู logs เฉพาะ container1
docker-compose logs container1

# ดู logs แบบ real-time
docker-compose logs -f
```

### หยุดและลบคอนเทนเนอร์
```bash
# หยุดคอนเทนเนอร์
docker-compose down

# หยุดและลบ volumes
docker-compose down -v

# หยุดและลบ images
docker-compose down --rmi all
```

### Restart บริการ
```bash
# Restart ทั้งหมด
docker-compose restart

# Restart เฉพาะ container1
docker-compose restart container1
```

##  การแก้ไขปัญหา

### ปัญหาที่อาจพบ

1. **Port ถูกใช้งานแล้ว**
   - ตรวจสอบว่า port 5000 หรือ 5001 ถูกใช้งานหรือไม่
   ```bash
   lsof -i :5000
   lsof -i :5001
   ```

2. **คอนเทนเนอร์ไม่สามารถติดต่อกันได้**
   - ตรวจสอบ network configuration
   ```bash
   docker network ls
   docker network inspect relax-app_relax-network
   ```

3. **Build ไม่สำเร็จ**
   - ลบ cache และ build ใหม่
   ```bash
   docker-compose build --no-cache
   ```

##  รายการกิจกรรมพักผ่อน

ระบบมีกิจกรรมพักผ่อนทั้งหมด 49 กิจกรรม เช่น:
- เดินเล่นรอบบ้าน
- อ่านหนังสือที่ชอบ
- ทำสมาธิ 10 นาที
- ฟังเพลงบรรเลง
- เล่นโยคะ
- และอื่นๆ อีกมากมาย

##  การปรับแต่ง

### เพิ่มกิจกรรมใหม่
แก้ไขไฟล์ `container2/app.py` ในส่วน `relax_activities` list

### เปลี่ยน Port
แก้ไข `docker-compose.yml` ในส่วน ports mapping

### เพิ่ม Environment Variables
เพิ่ม environment ใน `docker-compose.yml`:
```yaml
services:
  container1:
    environment:
      - ENV_VAR=value
```

