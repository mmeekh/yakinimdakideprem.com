/**
 * İstatistik Kartları Güncelleyici - JavaScript Modülü
 * Son 24 saat, 1 hafta ve 1 aylık deprem istatistiklerini günceller
 */

// İstatistik verilerini saklamak için (tek API çağrısından hesaplanacak)
let statisticsData = {
  allData: [], // 1 aylık tüm veri
  last24Hours: [],
  lastWeek: [],
  lastMonth: []
};

/**
 * Tek API çağrısı ile 1 aylık veriyi çeker ve diğer dönemleri hesaplar
 */
async function fetchAllStatistics() {
  try {
    // Sadece 1 aylık veri çek (sistemi zorlamamak için)
    const response = await fetch('/api/earthquakes?hours_back=720&min_magnitude=2.5&limit=500');
    const data = await response.json();
    
    if (data.success && data.data) {
      // Tüm veriyi sakla
      statisticsData.allData = data.data;
      
      // Zaman bazlı filtreleme yap
      const now = new Date();
      
      // Son 24 saat
      const last24Hours = new Date(now.getTime() - 24 * 60 * 60 * 1000);
      statisticsData.last24Hours = data.data.filter(eq => 
        new Date(eq.time) >= last24Hours
      );
      
      // Son 1 hafta
      const lastWeek = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      statisticsData.lastWeek = data.data.filter(eq => 
        new Date(eq.time) >= lastWeek
      );
      
      // Son 1 ay (zaten tüm veri)
      statisticsData.lastMonth = data.data;
      
      // Tüm ekranları güncelle
      updateAllDisplays();
    }
  } catch (error) {
    console.error('İstatistik verileri alınamadı:', error);
  }
}

/**
 * 24 saatlik istatistikleri günceller
 */
function update24HourDisplay() {
  const countNumber = document.querySelector('.daily-count .count-number');
  const averageNumber = document.querySelector('.hourly-average .average-number');
  
  if (countNumber && averageNumber) {
    const count = statisticsData.last24Hours.length;
    const hourlyAverage = (count / 24).toFixed(1);
    
    countNumber.textContent = count;
    averageNumber.textContent = hourlyAverage;
  }
}

/**
 * Haftalık istatistikleri günceller
 */
function updateWeeklyDisplay() {
  const totalNumber = document.querySelector('.weekly-stats .stat-item:first-child .stat-number');
  const dailyAverage = document.querySelector('.weekly-stats .stat-item:last-child .stat-number');
  
  if (totalNumber && dailyAverage) {
    const total = statisticsData.lastWeek.length;
    const dailyAvg = (total / 7).toFixed(1);
    
    totalNumber.textContent = total.toLocaleString('tr-TR');
    dailyAverage.textContent = dailyAvg;
  }
}

/**
 * Aylık istatistikleri günceller
 */
function updateMonthlyDisplay() {
  const totalNumber = document.querySelector('.monthly-stats .stat-item:first-child .stat-number');
  const dailyAverage = document.querySelector('.monthly-stats .stat-item:last-child .stat-number');
  
  if (totalNumber && dailyAverage) {
    const total = statisticsData.lastMonth.length;
    const dailyAvg = (total / 30).toFixed(1);
    
    totalNumber.textContent = total.toLocaleString('tr-TR');
    dailyAverage.textContent = dailyAvg;
  }
}

/**
 * Tüm ekranları günceller
 */
function updateAllDisplays() {
  update24HourDisplay();
  updateWeeklyDisplay();
  updateMonthlyDisplay();
}

/**
 * Tüm istatistikleri günceller (optimize edilmiş versiyon)
 */
async function updateAllStatistics() {
  await fetchAllStatistics();
}

/**
 * Sayfa yüklendiğinde çalışır
 */
document.addEventListener('DOMContentLoaded', () => {
  // Sayfa yüklendikten sonra kısa bir gecikme ile veri çek
  setTimeout(() => {
    updateAllStatistics();
  }, 1500); // Türkiye depremlerinden sonra

  // Her 10 dakikada bir güncelle (sistemi zorlamamak için)
  setInterval(() => {
    updateAllStatistics();
  }, 600000); // 10 dakika
});

// Global olarak erişilebilir yap
window.StatisticsUpdater = {
  update: updateAllStatistics,
  fetchAll: fetchAllStatistics,
  updateDisplays: updateAllDisplays
};
