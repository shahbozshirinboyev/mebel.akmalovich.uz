(function () {
  const formatNumber = (value) => {
    if (!value) return '';
    const cleaned = value.replace(/\s+/g, '').replace(/,/g, '');
    if (cleaned === '') return '';
    const parts = cleaned.split('.');
    const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    return parts.length > 1 ? `${integerPart}.${parts[1]}` : integerPart;
  };

  const bind = (input) => {
    if (input.dataset.thousandBound) return;
    input.dataset.thousandBound = 'true';
    input.addEventListener('input', (event) => {
      const caret = input.selectionStart;
      const formatted = formatNumber(input.value);
      if (formatted !== input.value) {
        input.value = formatted;
        if (caret !== null) {
          input.setSelectionRange(formatted.length, formatted.length);
        }
      }
    });
  };

  document.addEventListener('DOMContentLoaded', () => {
    const amountInputs = document.querySelectorAll('input[name$="_amount"], input[name*="amount"], input[name*="salary"], input[name*="total"]');
    amountInputs.forEach(bind);

    const forms = document.querySelectorAll('form');
    forms.forEach((form) => {
      form.addEventListener('submit', () => {
        amountInputs.forEach((input) => {
          if (input.value) {
            input.value = input.value.replace(/\s+/g, '').replace(/,/g, '');
          }
        });
      });
    });
  });
})();
