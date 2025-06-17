from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from .models import Category, Question
from datetime import datetime, timedelta

def get_daily_question(request, slug):
    session_key = f"viewed_{slug}"
    viewed_data = request.session.get(session_key)

    now = datetime.now()
    today = now.date()

    if viewed_data:
        viewed_time = datetime.fromisoformat(viewed_data['time'])
        if now - viewed_time < timedelta(days=1):
            seconds_left = int((viewed_time + timedelta(days=1) - now).total_seconds())
            return JsonResponse({
                'already_answered': True,
                'question': viewed_data['question'],
                'answer': viewed_data['answer'],
                'seconds_left': seconds_left,
                'error': "Siz bu kategoriyadan bugun savol oldingiz. Ertaga yana urinib ko‘ring."
            })

    try:
        category = Category.objects.get(slug=slug)
        questions = Question.objects.filter(category=category).order_by('id')
        if not questions.exists():
            return JsonResponse({'error': 'Bu kategoriya uchun savollar mavjud emas.'})

        index = today.toordinal() % questions.count()
        question = questions[index]

        # Saqlash
        request.session[session_key] = {
            'question': question.question,
            'answer': question.answer,
            'time': now.isoformat()
        }

        return JsonResponse({
            'question': question.question,
            'answer': question.answer,
            'already_answered': False
        })

    except Category.DoesNotExist:
        return JsonResponse({'error': 'Kategoriya topilmadi.'})

def daily_questions(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request,'index.html' , context)



# core/utils/sample_questions.py

sample_questions = [
    {"question": "Savol: C++ dasturlash tilida virtual destructor nima uchun kerak?", "answer": "Javob: Polimorfizmda to‘g‘ri destructor chaqirilishini ta’minlash uchun kerak."},
    {"question": "Savol: C++ da smart pointerlar (unique_ptr, shared_ptr, weak_ptr) farqi nima?", "answer": "Javob: unique_ptr – faqat bitta egalik, shared_ptr – ko‘p egalik, weak_ptr – shared_ptr’ga zaif bog‘lanish."},
    {"question": "Savol: RAII printsipi nima?", "answer": "Javob: Obyektlar resurslarni konstruktor orqali oladi va destruktor orqali ozod qiladi."},
    {"question": "Savol: C++ da template specialization nima?", "answer": "Javob: Shablonni ma’lum bir tur uchun alohida realizatsiya qilish usuli."},
    {"question": "Savol: `std::move()` funksiyasi nima qiladi?", "answer": "Javob: Rvalue reference yaratish orqali resurslarni ko‘chirishga yordam beradi."},
    {"question": "Savol: C++11 da lambda expression qanday yoziladi?", "answer": "Javob: `[capture](params) -> return_type {body}` shaklida yoziladi."},
    {"question": "Savol: `explicit` kalit so‘zi konstruktorda nima uchun ishlatiladi?", "answer": "Javob: Avtomatik tur o‘zgarishini oldini olish uchun."},
    {"question": "Savol: `friend` kalit so‘zining vazifasi nima?", "answer": "Javob: Private/protected bo‘limlarga boshqa klass/funksiya kirishiga ruxsat beradi."},
    {"question": "Savol: `std::vector` qanday konteyner va uning asosiy afzalliklari?", "answer": "Javob: Dinamik massiv bo‘lib, avtomatik o‘lcham oshishi, random access imkonini beradi."},
    {"question": "Savol: Operator overloading nima va qachon ishlatiladi?", "answer": "Javob: Operatorlarga o‘z sinfimiz uchun o‘ziga xos ma’no berish imkonini beradi."},
    {"question": "Savol: `std::map` va `std::unordered_map` o‘rtasidagi farq nima?", "answer": "Javob: `map` tartiblangan, `unordered_map` esa hash bilan tartiblanmagan lekin tezroq."},
    {"question": "Savol: `std::function` va `function pointer` farqi nima?", "answer": "Javob: `std::function` - har qanday chaqiriladigan obyektni saqlashi mumkin."},
    {"question": "Savol: C++ da slicing muammosi nima?", "answer": "Javob: Hosila klass obyektini asosiy klassga o‘tkazishda ma’lumotlar yo‘qotilishi."},
    {"question": "Savol: Copy constructor va move constructor farqi nima?", "answer": "Javob: Copy nusxa yaratadi, move esa mavjud resursni o‘zlashtiradi."},
    {"question": "Savol: Vtable nima va qanday ishlaydi?", "answer": "Javob: Virtual funksiyalar uchun ko‘rsatkichlar jadvali bo‘lib, run-time da funksiya chaqiradi."},
    {"question": "Savol: C++ da multiple inheritance qanday amalga oshiriladi?", "answer": "Javob: Klass bir nechta asosiy klasslardan meros ola oladi."},
    {"question": "Savol: `override` kalit so‘zining vazifasi nima?", "answer": "Javob: Virtual funksiyani hosila klassda qayta aniqlayotganimizni bildiradi."},
    {"question": "Savol: `mutable` kalit so‘zi nima qiladi?", "answer": "Javob: Const obyektlar ichida ham o‘zgartirilishi mumkin bo‘lgan o‘zgaruvchi e’lon qiladi."},
    {"question": "Savol: Exception handling qanday ishlaydi C++ da?", "answer": "Javob: `try-catch-throw` bloklari orqali xatoliklar ushlanadi va qayta ishlanadi."},
    {"question": "Savol: `noexcept` deklaratsiyasi nima qiladi?", "answer": "Javob: Funksiya hech qanday exception chiqarmasligini bildiradi."},
    {"question": "Savol: `std::unique_ptr` dan nusxa olish mumkinmi?", "answer": "Javob: Yo‘q, u faqat bitta obyektga egalik qiladi."},
    {"question": "Savol: `this` pointer qanday ishlaydi?", "answer": "Javob: Joriy obyektga ko‘rsatkich sifatida ishlaydi."},
    {"question": "Savol: `typeid` operatori nima qiladi?", "answer": "Javob: Ob’ektning real turini aniqlaydi."},
    {"question": "Savol: `dynamic_cast` qachon ishlatiladi?", "answer": "Javob: Polimorfik ko‘rsatkichlarni xavfsiz o‘tkazishda."},
    {"question": "Savol: Const correctness nima degani?", "answer": "Javob: Obyektlar, funksiyalar va ko‘rsatkichlarning o‘zgarmasligini aniq belgilash."},
    {"question": "Savol: `inline` funksiyalar qanday ishlaydi?", "answer": "Javob: Kompilyatsiya vaqtida kodga joylanadi, chaqirish emas."},
    {"question": "Savol: `constexpr` va `const` o‘rtasidagi farq nima?", "answer": "Javob: `constexpr` kompilyatsiya vaqtida aniqlanadi, `const` esa run-time ham bo‘lishi mumkin."},
    {"question": "Savol: Memory leak nima va uni qanday oldini olish mumkin?", "answer": "Javob: Ajratilgan xotiraning bo‘shatilmasligi; smart pointerlar bilan oldini olish mumkin."},
    {"question": "Savol: `std::tie` va `std::tuple` nima uchun kerak?", "answer": "Javob: Ko‘p qiymatni birgalikda uzatish yoki ajratish uchun."},
    {"question": "Savol: `volatile` kalit so‘zi nima qiladi?", "answer": "Javob: Kompilyator optimallashtirishdan saqlaydigan o‘zgaruvchi e’lon qiladi."},
    {"question": "Savol: `std::array` va `std::vector` o‘rtasidagi farq nima?", "answer": "Javob: `array` – statik o‘lcham, `vector` – dinamik o‘lcham."},
    {"question": "Savol: Pure virtual function qanday yoziladi?", "answer": "Javob: `virtual void func() = 0;`"},
    {"question": "Savol: Abstract klass nima?", "answer": "Javob: Kamida bitta pure virtual funksiyaga ega klass."},
    {"question": "Savol: Funksiya overload qilishda qanday cheklovlar bor?", "answer": "Javob: Parametrlar soni yoki turi bilan farqlanishi kerak, return turi bilan emas."},
    {"question": "Savol: `enum class` oddiy `enum`ga qaraganda qanday afzalliklarga ega?", "answer": "Javob: `enum class` kuchli tiplangan, nomlar global emas va xavfsiz."},
    {"question": "Savol: C++ da shallow copy va deep copy nima?", "answer": "Javob: Shallow – ko‘rsatkichni nusxalaydi, deep – yangi nusxa yaratadi."},
    {"question": "Savol: `std::initializer_list` nima?", "answer": "Javob: Obyektlarni ro‘yxat orqali berishga imkon beruvchi klass."},
    {"question": "Savol: `std::bind` funksiyasi nima uchun kerak?", "answer": "Javob: Funksiya argumentlarini oldindan biriktirish uchun."},
    {"question": "Savol: Funksiya pointerlari bilan `std::function` o‘rtasidagi afzalliklar?", "answer": "Javob: `std::function` lambdalarni, obyektlarni ham qo‘llab-quvvatlaydi."},
    {"question": "Savol: `std::chrono` kutubxonasi nimaga xizmat qiladi?", "answer": "Javob: Vaqtni o‘lchash va manipulyatsiya qilish uchun."},
    {"question": "Savol: `emplace_back()` va `push_back()` farqi nima?", "answer": "Javob: `emplace_back` obyektni joyida yaratadi, `push_back` esa nusxa kiritadi."},
    {"question": "Savol: Memory alignment nima degani?", "answer": "Javob: Obyektlar xotirada optimal joylashuvi uchun."},
    {"question": "Savol: Static polymorphism qanday amalga oshiriladi?", "answer": "Javob: Template va compile-time mexanizmlar orqali (CRTP)."},
    {"question": "Savol: `decltype` kalit so‘zi nima qiladi?", "answer": "Javob: O‘zgaruvchining turini aniqlaydi."},
    {"question": "Savol: C++ da move semantics nima?", "answer": "Javob: Resurslarni ko‘chirish orqali samaradorlikni oshirish."},
    {"question": "Savol: Const member functions qanday aniqlanadi?", "answer": "Javob: `void func() const;` – obyektni o‘zgartirmasligini bildiradi."},
    {"question": "Savol: Funksiya template’ga default parametr berish mumkinmi?", "answer": "Javob: Ha, lekin faqat oxirgi parametrdan boshlab."},
    {"question": "Savol: `std::optional` nima va qanday ishlatiladi?", "answer": "Javob: Qiymat bo‘lishi yoki bo‘lmasligini ifodalovchi konteyner."},
    {"question": "Savol: `alignas` va `alignof` kalit so‘zlari nima qiladi?", "answer": "Javob: `alignas` – obyekt uchun joylashuvni belgilaydi, `alignof` – mavjud obyekt joylashuvini qaytaradi."},
    {"question": "Savol: CRTP (Curiously Recurring Template Pattern) nima?", "answer": "Javob: Klass o‘zining template versiyasini meros qilib olishi."},
    {"question": "Savol: Polymorphism necha turga bo‘linadi C++ da?", "answer": "Javob: Compile-time (static) va run-time (dynamic) polymorphism."}
]




# def delete_sample_questions(request):
#     try:
#         # "react" slug'li category borligini tekshiramiz
#         category = Category.objects.filter(slug="react").first()
#         if not category:
#             return HttpResponse("Category topilmadi!")

#         deleted_count = 0

#         for item in sample_questions:
#             deleted, _ = Question.objects.filter(
#                 category=category,
#                 question=item["question"],
#                 answer=item["answer"]
#             ).delete()
#             deleted_count += deleted

#         return HttpResponse(f"{deleted_count} ta savol o‘chirildi.")

#     except Exception as e:
#         return HttpResponse(f"Xatolik: {str(e)}")



# def insert_sample_questions(request):
#     try:
#         category, created = Category.objects.get_or_create(
#             slug="cpp",  # slug URL uchun
#             defaults={"category": "Cpp", "img": "categories/default.jpg"}  # img sozlanmasa default rasm
#         )
#         for item in sample_questions:
#             Question.objects.get_or_create(
#                 category=category,
#                 question=item["question"],
#                 answer=item["answer"]
#             )

#         return HttpResponse("Savollar muvaffaqiyatli bazaga qo‘shildi!")

#     except Exception as e:
#         return HttpResponse(f"Xatolik: {str(e)}")
