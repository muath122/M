import pandas as pd
import streamlit as st
import time

# قراءة بيانات المباراة
def load_match_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        st.error(f"خطأ: الملف {file_path} غير موجود.")
        return None

# تحليل لحظة معينة
def analyze_weakness(row):
    failed_pass_rate = (row['failed_passes'] / row['total_passes']) * 100
    # لحظة ضعف: استحواذ < 40% ونسبة التمريرات الخاطئة > 40%
    if row['possession'] < 40 and failed_pass_rate > 40:
        return True, failed_pass_rate
    return False, failed_pass_rate

# الدالة الرئيسية
def main():
    st.title("نظام دعم القرارات التكتيكية في كرة القدم")
    st.write("جاري مراقبة المباراة لحظة بلحظة...")

    # إنشاء حاويات للإحصائيات والتنبيهات
    stats_placeholder = st.empty()
    alert_placeholder = st.empty()

    # قراءة البيانات
    data = load_match_data(r"C:\Users\yosef\Downloads\Telegram Desktop\match_stats.csv")
    if data is not None:
        # محاكاة التدفق اللحظي (دقيقة كل 3 ثوانٍ)
        for index, row in data.iterrows():
            # تحليل الدقيقة الحالية
            is_weak, failed_pass_rate = analyze_weakness(row)

            # عرض الإحصائيات
            stats_placeholder.write(
                f"**الدقيقة {int(row['minute'])}:** استحواذ {row['possession']}%, "
                f"تمريرات خاطئة {int(row['failed_passes'])}/{int(row['total_passes'])}, "
                f"نسبة التمريرات الخاطئة {failed_pass_rate:.1f}%"
            )

            # عرض التنبيه إذا وجدت لحظة ضعف
            if is_weak:
                alert_placeholder.error(
                    f"⚽ **تنبيه تكتيكي:** فرصة هجوم في الدقيقة {int(row['minute'])}! "
                    f"استحواذ {row['possession']}%, نسبة تمريرات خاطئة {failed_pass_rate:.1f}%"
                )
            else:
                alert_placeholder.success("لا توجد فرص هجومية واضحة في هذه الدقيقة.")

            # تأخير 3 ثوانٍ لمحاكاة الوقت الفعلي
            time.sleep(3)

if __name__ == "__main__":
    main()