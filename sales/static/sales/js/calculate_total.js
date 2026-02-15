// static/js/hisob.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('1. DOM yuklandi');

    // Barcha inputlarni topish
    const allInputs = document.querySelectorAll('input[type="number"]');
    console.log('2. Topilgan inputlar:', allInputs.length);

    allInputs.forEach((input, index) => {
        console.log(`Input ${index}:`, input.id, input.name, input.value);
    });

    // Aniq ID bilan qidirish
    const quantity = document.querySelector('#id_quantity, input[name="quantity"]');
    const price = document.querySelector('#id_price, input[name="price"]');

    console.log('3. Quantity:', quantity);
    console.log('4. Price:', price);

    if (quantity && price) {
        console.log('5. Inputlar topildi!');

        function hisobla() {
            const q = parseFloat(quantity.value) || 0;
            const p = parseFloat(price.value) || 0;
            const natija = (q * p).toFixed(2);
            console.log('6. Qiymatlar:', q, p, 'Natija:', natija);

            // Total maydonini yangilash
            const total = document.querySelector('#id_total, input[name="total"]');
            if (total) {
                total.value = natija;
                console.log('7. Total maydoni yangilandi:', natija);
            } else {
                console.error('Total maydoni topilmadi!');
            }
        }

        quantity.addEventListener('input', hisobla);
        price.addEventListener('input', hisobla);
    } else {
        console.error('Inputlar topilmadi!');
    }
});