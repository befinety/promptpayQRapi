# Thai PromptPay QR API - คู่มือการใช้งาน

## 🚀 เริ่มต้นใช้งานง่าย ๆ

### วิธีที่ 1: ใช้งานผ่าน Payload Converter (แนะนำ)
1. เปิดไฟล์ `payload_converter.html` ในเบราว์เซอร์
2. ใช้แท็บ "สร้าง Payload" เพื่อสร้าง QR Code
3. ใช้แท็บ "แปลง Payload" เพื่อแปลงข้อมูลกลับ
4. ใช้แท็บ "ทดสอบ" เพื่อตรวจสอบการทำงาน

### วิธีที่ 2: ใช้งานผ่าน QR Generator
1. เปิดไฟล์ `qr_final.html` ในเบราว์เซอร์
2. ใส่เบอร์โทรศัพท์หรือเลขประจำตัวผู้เสียภาษี
3. ใส่จำนวนเงิน (ไม่ใส่ก็ได้)
4. กดปุ่ม "สร้าง QR Code"
5. สแกน QR Code ด้วยแอป Banking

### วิธีที่ 3: ใช้งานผ่าน JavaScript API
```html
<!DOCTYPE html>
<html>
<head>
    <title>PromptPay QR</title>
</head>
<body>
    <div id="qr-display"></div>
    
    <script src="thaipromptpayapi.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>
    <script>
        // สร้าง QR Code สำหรับเบอร์โทรศัพท์
        const payload = ThaiPromptPayAPI.generateFromPhoneNumber('0812345678', 100.00);
        
        // สร้าง QR Code
        const qr = qrcode(0, 'M');
        qr.addData(payload);
        qr.make();
        
        // แสดงผล QR Code
        document.getElementById('qr-display').innerHTML = qr.createImgTag(4);
    </script>
</body>
</html>
```

## 📚 API Reference

### การสร้าง Payload

#### `ThaiPromptPayAPI.generatePayload(target, amount)`
สร้าง PromptPay payload สำหรับทุกประเภท

**Parameters:**
- `target` (string): เบอร์โทรศัพท์, เลขประจำตัวผู้เสียภาษี, หรือ e-Wallet ID
- `amount` (number, optional): จำนวนเงิน (บาท)

**Returns:** `string` - PromptPay payload

**ตัวอย่าง:**
```javascript
// QR Code แบบไม่มีจำนวนเงิน (Static QR)
const staticQR = ThaiPromptPayAPI.generatePayload('0812345678');

// QR Code แบบมีจำนวนเงิน (Dynamic QR)
const dynamicQR = ThaiPromptPayAPI.generatePayload('0812345678', 150.00);
```

#### `ThaiPromptPayAPI.generateFromPhoneNumber(phoneNumber, amount)`
สร้าง payload สำหรับเบอร์โทรศัพท์

**Parameters:**
- `phoneNumber` (string): เบอร์โทรศัพท์ไทย
- `amount` (number, optional): จำนวนเงิน

**ตัวอย่าง:**
```javascript
const payload = ThaiPromptPayAPI.generateFromPhoneNumber('0812345678', 50.00);
```

#### `ThaiPromptPayAPI.generateFromTaxId(taxId, amount)`
สร้าง payload สำหรับเลขประจำตัวผู้เสียภาษี

**Parameters:**
- `taxId` (string): เลขประจำตัวผู้เสียภาษี (13 หลัก)
- `amount` (number, optional): จำนวนเงิน

**ตัวอย่าง:**
```javascript
const payload = ThaiPromptPayAPI.generateFromTaxId('1234567890123', 200.00);
```

#### `ThaiPromptPayAPI.validateTarget(target)`
ตรวจสอบความถูกต้องของเป้าหมาย

**Parameters:**
- `target` (string): เบอร์โทรศัพท์หรือเลขประจำตัวผู้เสียภาษี

**Returns:** `object`
- `isValid` (boolean): ถูกต้องหรือไม่
- `type` (string): ประเภท ('phone', 'taxid', 'ewallet', 'unknown')

**ตัวอย่าง:**
```javascript
const validation = ThaiPromptPayAPI.validateTarget('0812345678');
console.log(validation); // { isValid: true, type: 'phone' }
```

### การแปลง Payload (ใหม่!)

#### `ThaiPromptPayAPI.parsePayload(payload)`
แปลง payload เป็นข้อมูลรายละเอียด

**Parameters:**
- `payload` (string): PromptPay payload string

**Returns:** `object` - ข้อมูลที่แปลงแล้ว

**ตัวอย่าง:**
```javascript
const parsed = ThaiPromptPayAPI.parsePayload(payload);
console.log(parsed.target); // '0812345678'
console.log(parsed.amount); // 100.00
console.log(parsed.targetType); // 'phone'
```

#### `ThaiPromptPayAPI.decodePayload(payload)`
แปลง payload เป็นข้อมูลที่อ่านง่าย

**Parameters:**
- `payload` (string): PromptPay payload string

**Returns:** `object` - ข้อมูลที่แปลงแล้ว

**ตัวอย่าง:**
```javascript
const decoded = ThaiPromptPayAPI.decodePayload(payload);
console.log(decoded.target); // '0812345678'
console.log(decoded.targetTypeText); // 'เบอร์โทรศัพท์'
console.log(decoded.amount); // 100.00
console.log(decoded.isStatic); // false
console.log(decoded.isDynamic); // true
```

#### `ThaiPromptPayAPI.payloadToReadable(payload)`
แปลง payload เป็นข้อความที่อ่านง่าย

**Parameters:**
- `payload` (string): PromptPay payload string

**Returns:** `string` - ข้อความภาษาไทย

**ตัวอย่าง:**
```javascript
const readable = ThaiPromptPayAPI.payloadToReadable(payload);
console.log(readable);
/*
PromptPay QR Code Information:
- Target: 0812345678 (เบอร์โทรศัพท์)
- Amount: 100.00 THB
- Type: Dynamic QR (จำนวนเงินคงที่)
- Country: TH
- Currency: 764
*/
```

## 🎯 ตัวอย่างการใช้งาน

### 1. QR Code สำหรับร้านค้า
```javascript
// QR Code แบบไม่มีจำนวนเงิน - ลูกค้าใส่จำนวนเอง
const shopQR = ThaiPromptPayAPI.generateFromPhoneNumber('0812345678');
```

### 2. QR Code สำหรับบิล
```javascript
// QR Code แบบมีจำนวนเงิน - จำนวนเงินคงที่
const billQR = ThaiPromptPayAPI.generateFromPhoneNumber('0812345678', 1250.00);
```

### 3. QR Code สำหรับองค์กร
```javascript
// ใช้เลขประจำตัวผู้เสียภาษี
const orgQR = ThaiPromptPayAPI.generateFromTaxId('1234567890123', 500.00);
```

### 4. การแปลง Payload กลับ
```javascript
// สร้าง payload
const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100.00);

// แปลง payload กลับ
const decoded = ThaiPromptPayAPI.decodePayload(payload);
console.log(`เป้าหมาย: ${decoded.target}`);
console.log(`จำนวนเงิน: ${decoded.amount} บาท`);
console.log(`ประเภท: ${decoded.targetTypeText}`);
```

### 5. การตรวจสอบและแปลงแบบปลอดภัย
```javascript
function processQRPayload(payload) {
    try {
        // แปลง payload
        const decoded = ThaiPromptPayAPI.decodePayload(payload);
        
        if (!decoded.success) {
            throw new Error(decoded.error);
        }
        
        // ตรวจสอบความถูกต้อง
        const validation = ThaiPromptPayAPI.validateTarget(decoded.target);
        
        if (!validation.isValid) {
            throw new Error('เป้าหมายไม่ถูกต้อง');
        }
        
        return {
            target: decoded.target,
            amount: decoded.amount,
            type: decoded.targetTypeText,
            isStatic: decoded.isStatic
        };
        
    } catch (error) {
        console.error('ข้อผิดพลาด:', error.message);
        return null;
    }
}
```

### 6. การสร้างและแปลงแบบสมบูรณ์
```javascript
function createAndVerifyQR(target, amount) {
    // สร้าง payload
    const payload = ThaiPromptPayAPI.generatePayload(target, amount);
    
    // แปลง payload กลับเพื่อตรวจสอบ
    const decoded = ThaiPromptPayAPI.decodePayload(payload);
    
    // ตรวจสอบความถูกต้อง
    const isValid = decoded.success && 
                   decoded.target === target && 
                   decoded.amount === amount;
    
    return {
        payload: payload,
        isValid: isValid,
        info: decoded
    };
}
```

## 🔧 การติดตั้งและใช้งาน

### Browser
```html
<!-- โหลด JavaScript files -->
<script src="thaipromptpayapi.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcode-generator/1.4.4/qrcode.min.js"></script>

<script>
    // สร้าง payload
    const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100);
    
    // แปลง payload กลับ
    const decoded = ThaiPromptPayAPI.decodePayload(payload);
</script>
```

### Node.js
```javascript
// ติดตั้ง dependencies
npm install qrcode

// ใช้งาน
const ThaiPromptPayAPI = require('./thaipromptpayapi.js');
const QRCode = require('qrcode');

// สร้าง payload
const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100);

// แปลง payload กลับ
const decoded = ThaiPromptPayAPI.decodePayload(payload);
console.log(decoded);

// สร้าง QR Code
QRCode.toString(payload, { type: 'terminal' }, console.log);
```

## 📱 รูปแบบเป้าหมายที่รองรับ

### เบอร์โทรศัพท์
- **รูปแบบ:** 9-12 หลัก
- **ตัวอย่าง:** `0812345678`, `66812345678`, `812345678`
- **หมายเหตุ:** ระบบจะแปลงเป็น format มาตรฐานอัตโนมัติ

### เลขประจำตัวผู้เสียภาษี
- **รูปแบบ:** 13 หลัก
- **ตัวอย่าง:** `1234567890123`
- **หมายเหตุ:** สำหรับบุคคลธรรมดาหรือนิติบุคคล

### e-Wallet ID
- **รูปแบบ:** 15+ หลัก
- **ตัวอย่าง:** `123456789012345`
- **หมายเหตุ:** สำหรับ e-Wallet ที่รองรับ PromptPay

## 🧪 การทดสอบ

### ทดสอบ API
```javascript
// ทดสอบการสร้าง payload
console.log('Phone:', ThaiPromptPayAPI.generateFromPhoneNumber('0812345678'));
console.log('Tax ID:', ThaiPromptPayAPI.generateFromTaxId('1234567890123'));

// ทดสอบการแปลง payload
const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100);
const decoded = ThaiPromptPayAPI.decodePayload(payload);
console.log('Decoded:', decoded);

// ทดสอบการตรวจสอบ
console.log('Validation:', ThaiPromptPayAPI.validateTarget('0812345678'));
```

### ทดสอบ QR Code
1. เปิด `qr_final.html` หรือ `payload_converter.html` ในเบราว์เซอร์
2. ใส่ข้อมูลทดสอบ
3. สแกน QR Code ด้วยแอป Banking
4. ตรวจสอบความถูกต้อง

### ทดสอบ Payload Converter
1. เปิด `payload_converter.html`
2. ใช้แท็บ "สร้าง Payload" สร้าง QR Code
3. คัดลอก payload ที่ได้
4. ใช้แท็บ "แปลง Payload" แปลงกลับ
5. ตรวจสอบว่าข้อมูลตรงกัน

### แอปที่ใช้ทดสอบได้
- 🏦 K PLUS (กสิกรไทย)
- 🏦 SCB EASY (ไทยพาณิชย์)
- 🏦 Krungsri (กรุงศรี)
- 🏦 KTB netbank (กรุงไทย)
- 💳 TrueMoney Wallet
- 📱 แอป QR Scanner ทั่วไป

## 🔍 Payload Structure

PromptPay payload ประกอบด้วย:

```
Field | Length | Description
------|--------|------------
00    | 02     | Payload Format (01)
01    | 02     | POI Method (11=Static, 12=Dynamic)
29    | 37     | Merchant Info (PromptPay)
58    | 02     | Country Code (TH)
53    | 03     | Currency (764=THB)
54    | 06     | Amount (ถ้ามี)
63    | 04     | CRC16 Checksum
```

### ตัวอย่าง Payload
```javascript
// เบอร์โทรศัพท์ไม่มีจำนวนเงิน
const staticPayload = "00020101011102160016A00000067701011101300066812345678058027653037640630445C4";

// เบอร์โทรศัพท์มีจำนวนเงิน 100 บาท
const dynamicPayload = "00020101021102160016A00000067701011101300066812345678058027653037645406100.0063043A8F";

// แปลง payload กลับ
const decoded1 = ThaiPromptPayAPI.decodePayload(staticPayload);
const decoded2 = ThaiPromptPayAPI.decodePayload(dynamicPayload);
```

## 🚨 ข้อจำกัดและข้อควรระวัง

### ข้อจำกัด
- จำนวนเงินต้องเป็นตัวเลขบวก
- รองรับเฉพาะสกุลเงินบาทไทย (THB)
- เบอร์โทรศัพท์ต้องเป็นเบอร์ไทย

### ข้อควรระวัง
- ตรวจสอบความถูกต้องของข้อมูลก่อนสร้าง QR Code
- ทดสอบ QR Code ก่อนนำไปใช้งานจริง
- ใช้ HTTPS เมื่อโฮสต์บนเซิร์ฟเวอร์
- ตรวจสอบ payload ที่ได้รับจากแหล่งภายนอก

## 🔧 Troubleshooting

### ปัญหาที่พบบ่อย

**1. QR Code ไม่แสดง**
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- ตรวจสอบว่าโหลด QR Code library แล้ว

**2. QR Code สแกนไม่ได้**
- ตรวจสอบความถูกต้องของเบอร์โทรศัพท์
- ใช้ `qr_final.html` หรือ `payload_converter.html`

**3. Payload ไม่ถูกต้อง**
```javascript
// ตรวจสอบ payload
const payload = ThaiPromptPayAPI.generatePayload('0812345678', 100);
console.log('Payload:', payload);
console.log('Length:', payload.length);

// ตรวจสอบการแปลงกลับ
const decoded = ThaiPromptPayAPI.decodePayload(payload);
console.log('Decoded:', decoded);
```

**4. การแปลง Payload ล้มเหลว**
```javascript
try {
    const decoded = ThaiPromptPayAPI.decodePayload(payload);
    if (decoded.success) {
        console.log('Success:', decoded);
    } else {
        console.error('Decode failed:', decoded.error);
    }
} catch (error) {
    console.error('Error:', error.message);
}
```

**5. การตรวจสอบ errors**
```javascript
function safeGeneratePayload(target, amount) {
    try {
        // ตรวจสอบเป้าหมาย
        const validation = ThaiPromptPayAPI.validateTarget(target);
        if (!validation.isValid) {
            throw new Error(`Invalid target: ${target}`);
        }
        
        // สร้าง payload
        const payload = ThaiPromptPayAPI.generatePayload(target, amount);
        
        // ตรวจสอบ payload
        const decoded = ThaiPromptPayAPI.decodePayload(payload);
        if (!decoded.success) {
            throw new Error(`Invalid payload: ${decoded.error}`);
        }
        
        return { success: true, payload: payload, info: decoded };
    } catch (error) {
        return { success: false, error: error.message };
    }
}
```

## 📋 Checklist การใช้งาน

### การสร้าง QR Code
- [ ] ใช้ไฟล์ `qr_final.html` หรือ `payload_converter.html`
- [ ] ใช้ `thaipromptpayapi.js` สำหรับ API
- [ ] ตรวจสอบความถูกต้องของเบอร์โทรศัพท์
- [ ] ทดสอบ QR Code ด้วยแอป Banking
- [ ] ตรวจสอบจำนวนเงินให้ถูกต้อง

### การแปลง Payload
- [ ] ใช้ `decodePayload()` สำหรับแปลงข้อมูล
- [ ] ตรวจสอบ `success` property
- [ ] ตรวจสอบข้อมูลที่แปลงได้
- [ ] ทดสอบด้วย payload ที่รู้จัก

### การพัฒนา
- [ ] ใช้ HTTPS เมื่อโฮสต์จริง
- [ ] ตรวจสอบ error handling
- [ ] ทดสอบกับข้อมูลหลายประเภท
- [ ] ตรวจสอบความปลอดภัยของข้อมูล

## 🎯 Best Practices

### 1. Error Handling
```javascript
function generateQRSafely(target, amount) {
    try {
        const validation = ThaiPromptPayAPI.validateTarget(target);
        if (!validation.isValid) {
            throw new Error(`Invalid ${validation.type}`);
        }
        
        const payload = ThaiPromptPayAPI.generatePayload(target, amount);
        const decoded = ThaiPromptPayAPI.decodePayload(payload);
        
        if (!decoded.success) {
            throw new Error(`Invalid payload: ${decoded.error}`);
        }
        
        return { success: true, payload: payload, info: decoded };
    } catch (error) {
        console.error('QR Generation failed:', error.message);
        return { success: false, error: error.message };
    }
}
```

### 2. Input Validation
```javascript
function validateInput(target, amount) {
    if (!target || target.trim() === '') {
        return { valid: false, message: 'เบอร์โทรศัพท์ว่างเปล่า' };
    }
    
    if (amount && (amount <= 0 || amount > 1000000)) {
        return { valid: false, message: 'จำนวนเงินไม่ถูกต้อง' };
    }
    
    const validation = ThaiPromptPayAPI.validateTarget(target);
    if (!validation.isValid) {
        return { valid: false, message: 'รูปแบบเป้าหมายไม่ถูกต้อง' };
    }
    
    return { valid: true };
}
```

### 3. Payload Conversion
```javascript
function convertPayload(payload) {
    try {
        const decoded = ThaiPromptPayAPI.decodePayload(payload);
        
        if (!decoded.success) {
            throw new Error(decoded.error);
        }
        
        return {
            target: decoded.target,
            targetType: decoded.targetType,
            targetTypeText: decoded.targetTypeText,
            amount: decoded.amount,
            currency: decoded.currency,
            countryCode: decoded.countryCode,
            isStatic: decoded.isStatic,
            isDynamic: decoded.isDynamic,
            readable: ThaiPromptPayAPI.payloadToReadable(payload)
        };
    } catch (error) {
        return { error: error.message };
    }
}
```

### 4. QR Code Generation
```javascript
function createQRCode(payload, containerId) {
    try {
        const qr = qrcode(0, 'M');
        qr.addData(payload);
        qr.make();
        
        document.getElementById(containerId).innerHTML = qr.createImgTag(4);
        return true;
    } catch (error) {
        console.error('QR Code generation failed:', error);
        return false;
    }
}
```

## 📞 Support

หากพบปัญหาหรือต้องการความช่วยเหลือ:
- ตรวจสอบ console errors ในเบราว์เซอร์
- ทดสอบด้วย `payload_converter.html` หรือ `qr_final.html`
- ตรวจสอบ payload ด้วย `decodePayload()`
- ใช้ `validateTarget()` เพื่อตรวจสอบเป้าหมาย

## 🆕 อัปเดตล่าสุด

### เวอร์ชัน 2.0.0
- ✅ เพิ่มฟังก์ชัน `parsePayload()` สำหรับแปลง payload
- ✅ เพิ่มฟังก์ชัน `decodePayload()` สำหรับแปลงข้อมูล
- ✅ เพิ่มฟังก์ชัน `payloadToReadable()` สำหรับข้อความที่อ่านง่าย
- ✅ สร้าง `payload_converter.html` สำหรับทดสอบ
- ✅ ปรับปรุง error handling
- ✅ เพิ่มการทดสอบแบบครบถ้วน

### ไฟล์ที่พร้อมใช้งาน
- `thaipromptpayapi.js` - API หลักพร้อมฟังก์ชัน converter
- `qr_final.html` - สร้าง QR Code ที่สแกนได้
- `payload_converter.html` - แปลง payload ไปมาได้
- `howtoqrapi.md` - คู่มือการใช้งาน

---

**หมายเหตุ:** คู่มือนี้อัปเดตสำหรับเวอร์ชันล่าสุดที่มีฟังก์ชัน Payload Converter ใช้ไฟล์ `payload_converter.html` สำหรับการทดสอบที่ดีที่สุด