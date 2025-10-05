document.addEventListener('DOMContentLoaded', function () {
    // Parse data passed from Flask
    const categoryData = JSON.parse(document.querySelector('script[type="application/json"][id="categoryData"]').textContent);
    const monthlyData = JSON.parse(document.querySelector('script[type="application/json"][id="monthlyData"]').textContent);
    const incomeCategoryData = JSON.parse(document.querySelector('script[type="application/json"][id="incomeCategoryData"]').textContent);
    const monthlyIncomeData = JSON.parse(document.querySelector('script[type="application/json"][id="monthlyIncomeData"]').textContent);

    // Prepare data for category chart
    const categories = categoryData.map(item => item[0]);
    const categoryAmounts = categoryData.map(item => item[1]);

    // Prepare data for monthly chart
    const months = monthlyData.map(item => item[0]);
    const monthlyAmounts = monthlyData.map(item => item[1]);

    // Prepare data for income category chart
    const incomeCategories = incomeCategoryData.map(item => item[0]);
    const incomeCategoryAmounts = incomeCategoryData.map(item => item[1]);

    // Prepare data for monthly income chart
    const incomeMonths = monthlyIncomeData.map(item => item[0]);
    const monthlyIncomeAmounts = monthlyIncomeData.map(item => item[1]);

    // Category Pie Chart
    const ctxCategory = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctxCategory, {
        type: 'pie',
        data: {
            labels: categories,
            datasets: [{
                data: categoryAmounts,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#C9CBCF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });

    // Monthly Bar Chart
    const ctxMonthly = document.getElementById('monthlyChart').getContext('2d');
    new Chart(ctxMonthly, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Expenses',
                data: monthlyAmounts,
                backgroundColor: '#36A2EB'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Income Category Pie Chart
    const ctxIncomeCategory = document.getElementById('incomeCategoryChart').getContext('2d');
    new Chart(ctxIncomeCategory, {
        type: 'pie',
        data: {
            labels: incomeCategories,
            datasets: [{
                data: incomeCategoryAmounts,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#C9CBCF'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });

    // Monthly Income Bar Chart
    const ctxMonthlyIncome = document.getElementById('monthlyIncomeChart').getContext('2d');
    new Chart(ctxMonthlyIncome, {
        type: 'bar',
        data: {
            labels: incomeMonths,
            datasets: [{
                label: 'Income',
                data: monthlyIncomeAmounts,
                backgroundColor: '#4BC0C0'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
