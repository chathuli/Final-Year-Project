# Symptom Analysis History Feature - සිංහල සාරාංශය

## කළ වෙනස්කම්

History page එකට Symptom Analysis කොටසින් කරන predictions වල සම්පූර්ණ විස්තර පෙන්වන්න update කරා.

## ප්‍රධාන වෙනස්කම්

### 1. Database එකට අලුත් columns තුනක් එකතු කළා:
- **prediction_type**: Prediction එක symptom-based ද manual input ද කියලා හඳුනාගන්න
- **symptoms_data**: රෝගියා දුන් සියලුම symptoms තොරතුරු save කරන්න
- **risk_assessment**: Risk assessment එකේ results save කරන්න

### 2. History Page එකේ අලුත් features:

#### Type Column (නව තීරුව)
- 🩺 **Symptom Analysis** (නිල් badge): Symptom checker එකෙන් කළ predictions
- 📊 **Manual Input** (අළු badge): සෘජුවම features දාලා කළ predictions

#### Risk Level Column (අලුත් තීරුව)
Risk assessment එක color-coded badges වලින් පෙන්වනවා:
- 🔴 **Very High**: හදිසි වෛද්‍ය ප්‍රතිකාර අවශ්‍යයි
- 🟠 **High**: වහාම වෛද්‍යවරයෙකු만ණන්න
- 🔵 **Moderate**: ඉක්මනින් වෛද්‍යවරයෙකු මණන්න
- 🟢 **Low-Moderate**: පරීක්ෂණයක් කරන්න සලකා බලන්න
- 🟢 **Low**: නිතිපතා self-examinations කරගෙන යන්න
- ⚪ **N/A**: Manual predictions වලට අදාළ නැහැ

#### View Details Button (විස්තර බලන්න බොත්තම)
Symptom-based predictions වලට "👁️ View Details" click කරන්න පුළුවන්. එතකොට පෙන්වන්නේ:

**රෝගියාගේ තොරතුරු:**
- වයස
- පවුලේ ඉතිහාසය
- ඔසප් තත්වය
- ගැබ් ඉතිහාසය
- පෙර පියයුරු රෝග

**ශාරීරික රෝග ලක්ෂණ:**
- ගැටිති (ප්‍රමාණය සහ චලනය)
- අත් යට ගැටිති
- වේදනාව (තීව්‍රතාවය සහ කාලය)
- සමේ වෙනස්කම්
- සමේ වයනය
- තන පුඩුව ස්‍රාවය
- තන පුඩුව ආපසු යෑම
- පියයුරු හැඩයේ වෙනස්කම්
- රෝග ලක්ෂණ කාලය

**අවදානම් තක්සේරුව:**
- අවදානම් මට්ටම සහ ලකුණු
- හඳුනාගත් සියලුම අවදානම් සාධක
- වෛද්‍ය නිර්දේශ

## භාවිතා කරන්නේ කෙසේද

### රෝගීන්ට:
1. Navigation menu එකෙන් **History** page එකට යන්න
2. ඔබේ සියලුම predictions වර්ග සහ අවදානම් මට්ටම් සමඟ බලන්න
3. Symptom-based predictions වලට **"👁️ View Details"** click කරලා බලන්න:
   - ඔබ වාර්තා කළ රෝග ලක්ෂණ
   - ඔබේ අවදානම් තක්සේරුව
   - වෛද්‍ය නිර්දේශ
4. සාමාන්‍ය විදියට **"📄 Download Report"** button එකෙන් reports download කරන්න

### වෛද්‍යවරුන්ට/Admins ට:
- Risk Level column එක බලලා ඉක්මනින් high-risk cases හඳුනාගන්න
- වඩා හොඳ රෝගී තක්සේරුවක් සඳහා සම්පූර්ණ symptom history බලන්න
- Symptom analysis වලින් ආපු predictions සහ manual input වලින් ආපු predictions track කරන්න
- අවශ්‍ය නම් predictions delete කරන්න (admin පමණයි)

## Migration කරන්නේ කෙසේද

දැනට තියෙන installation එකක් තියෙනවා නම්, මේක run කරන්න:
```bash
python migrate_database.py
```

මේකෙන් වෙන්නේ:
- දැනට තියෙන database එකට අලුත් columns එකතු කරනවා
- පැරණි data කිසිවක් නැති වෙන්නේ නැහැ
- පැරණි predictions වලට default values set කරනවා

## Test කරන්නේ කෙසේද

Feature එක හරියට වැඩ කරනවාද කියලා test කරන්න:
```bash
python test_symptom_history.py
```

මේකෙන් වෙන්නේ:
- Test symptom-based prediction එකක් create කරනවා
- Data හරියට save වුනාද කියලා verify කරනවා
- Prediction එක retrieve කරලා display කරනවා
- Prediction types අනුව statistics පෙන්වනවා

## වාසි

✅ **සම්පූර්ණ Audit Trail** - වාර්තා කළ සෑම රෝග ලක්ෂණයක්ම save වෙලා review කරන්න පුළුවන්
✅ **අවදානම් දෘශ්‍යතාව** - එක බැල්මකින් risk levels බලන්න පුළුවන්
✅ **වඩා හොඳ රෝගී සත්කාරය** - වෛද්‍යවරුන්ට සම්පූර්ණ symptom history review කරන්න පුළුවන්
✅ **දත්ත විශ්ලේෂණය** - Symptom-based predictions වල patterns track කරන්න පුළුවන්
✅ **විනිවිදභාවය** - රෝගීන්ට ඔවුන් වාර්තා කළ දේ review කරන්න පුළුවන්
✅ **Backward Compatible** - පැරණි predictions තවමත් හොඳින් වැඩ කරනවා

## තත්වය

✅ Database schema update කරා
✅ Migration script create කරලා test කරා
✅ API endpoints update කරා
✅ UI එකට අලුත් columns සහ modal එකතු කරා
✅ Test script create කරලා pass වෙනවා
✅ Documentation සම්පූර්ණයි

**Production භාවිතය සඳහා සූදානම්!**

## උදාහරණය

History page එකේ දැන් පෙන්වන්නේ මෙහෙමයි:

```
╔════╦═══════════════════════╦═══════════════════════╦════════════╦════════════╦══════════════╦════════╦═══════════════════════════╗
║ ID ║ Date & Time           ║ Type                  ║ Prediction ║ Confidence ║ Risk Level   ║ Model  ║ Actions                   ║
╠════╬═══════════════════════╬═══════════════════════╬════════════╬════════════╬══════════════╬════════╬═══════════════════════════╣
║ 52 ║ 4/29/2026, 2:18:00 PM ║ 🩺 Symptom Analysis   ║ Benign     ║ 85.0%      ║ Moderate     ║ RF     ║ 👁️ View | 📄 Download    ║
║ 51 ║ 4/29/2026, 2:16:07 PM ║ 📊 Manual Input       ║ Malignant  ║ 98.8%      ║ N/A          ║ RF     ║ 📄 Download              ║
╚════╩═══════════════════════╩═══════════════════════╩════════════╩════════════╩══════════════╩════════╩═══════════════════════════╝
```

## සාරාංශය

Symptom Analysis කොටසින් කරන predictions වල සියලුම තොරතුරු (symptoms, risk assessment, recommendations) දැන් History page එකේ පෙන්වනවා. රෝගීන්ට සහ වෛද්‍යවරුන්ට වඩා හොඳ අත්දැකීමක් ලබා දෙනවා.
