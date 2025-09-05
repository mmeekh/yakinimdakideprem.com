/**
 * Stats Module - Anlık Deprem
 * Handles statistics calculation and display
 */

class StatsModule {
  constructor(app) {
    this.app = app;
  }

  /**
   * Update all statistics
   */
  updateStats() {
    this.updateDailyCount();
    this.updateMaxMagnitude();
    this.updateLastUpdateTime();
  }

  /**
   * Update daily earthquake count
   */
  updateDailyCount() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const todayQuakes = this.app.state.earthquakeData.filter(eq => {
      const eqDate = new Date(eq.time);
      eqDate.setHours(0, 0, 0, 0);
      return eqDate.getTime() === today.getTime();
    });

    const dailyQuakesEl = document.getElementById('daily-quakes');
    if (dailyQuakesEl) {
      dailyQuakesEl.textContent = todayQuakes.length;
    }

    this.app.emit('stats:daily:updated', todayQuakes.length);
  }

  /**
   * Update maximum magnitude
   */
  updateMaxMagnitude() {
    if (this.app.state.earthquakeData.length === 0) return;

    const maxMag = Math.max(...this.app.state.earthquakeData.map(eq => eq.magnitude));
    const maxMagnitudeEl = document.getElementById('max-magnitude');
    
    if (maxMagnitudeEl) {
      maxMagnitudeEl.textContent = maxMag.toFixed(1);
    }

    this.app.emit('stats:maxmagnitude:updated', maxMag);
  }

  /**
   * Update last update time
   */
  updateLastUpdateTime() {
    const lastUpdateTimeEl = document.getElementById('last-update-time');
    if (lastUpdateTimeEl && this.app.state.lastUpdateTime) {
      const timeString = this.app.state.lastUpdateTime.toLocaleTimeString('tr-TR');
      lastUpdateTimeEl.textContent = timeString;
    }
  }

  /**
   * Get earthquake statistics
   */
  getStatistics() {
    const data = this.app.state.earthquakeData;
    
    if (data.length === 0) {
      return {
        total: 0,
        today: 0,
        maxMagnitude: 0,
        minMagnitude: 0,
        averageMagnitude: 0,
        byMagnitude: {},
        byHour: {},
        byDepth: {}
      };
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const todayQuakes = data.filter(eq => {
      const eqDate = new Date(eq.time);
      eqDate.setHours(0, 0, 0, 0);
      return eqDate.getTime() === today.getTime();
    });

    const magnitudes = data.map(eq => eq.magnitude);
    const depths = data.map(eq => eq.depth);

    return {
      total: data.length,
      today: todayQuakes.length,
      maxMagnitude: Math.max(...magnitudes),
      minMagnitude: Math.min(...magnitudes),
      averageMagnitude: this.calculateAverage(magnitudes),
      byMagnitude: this.groupByMagnitude(data),
      byHour: this.groupByHour(data),
      byDepth: this.groupByDepth(data)
    };
  }

  /**
   * Calculate average value
   */
  calculateAverage(values) {
    return values.reduce((sum, value) => sum + value, 0) / values.length;
  }

  /**
   * Group earthquakes by magnitude ranges
   */
  groupByMagnitude(data) {
    const ranges = {
      '2.0-3.0': 0,
      '3.0-4.0': 0,
      '4.0-5.0': 0,
      '5.0-6.0': 0,
      '6.0+': 0
    };

    data.forEach(eq => {
      const mag = eq.magnitude;
      if (mag >= 2.0 && mag < 3.0) ranges['2.0-3.0']++;
      else if (mag >= 3.0 && mag < 4.0) ranges['3.0-4.0']++;
      else if (mag >= 4.0 && mag < 5.0) ranges['4.0-5.0']++;
      else if (mag >= 5.0 && mag < 6.0) ranges['5.0-6.0']++;
      else if (mag >= 6.0) ranges['6.0+']++;
    });

    return ranges;
  }

  /**
   * Group earthquakes by hour of day
   */
  groupByHour(data) {
    const hours = {};
    
    for (let i = 0; i < 24; i++) {
      hours[i] = 0;
    }

    data.forEach(eq => {
      const hour = new Date(eq.time).getHours();
      hours[hour]++;
    });

    return hours;
  }

  /**
   * Group earthquakes by depth ranges
   */
  groupByDepth(data) {
    const ranges = {
      '0-10km': 0,
      '10-30km': 0,
      '30-50km': 0,
      '50km+': 0
    };

    data.forEach(eq => {
      const depth = eq.depth;
      if (depth >= 0 && depth < 10) ranges['0-10km']++;
      else if (depth >= 10 && depth < 30) ranges['10-30km']++;
      else if (depth >= 30 && depth < 50) ranges['30-50km']++;
      else if (depth >= 50) ranges['50km+']++;
    });

    return ranges;
  }

  /**
   * Get recent earthquakes (last N hours)
   */
  getRecentEarthquakes(hours = 24) {
    const cutoffTime = new Date(Date.now() - hours * 3600000);
    return this.app.state.earthquakeData.filter(eq => eq.time >= cutoffTime);
  }

  /**
   * Get strongest earthquakes
   */
  getStrongestEarthquakes(limit = 10) {
    return [...this.app.state.earthquakeData]
      .sort((a, b) => b.magnitude - a.magnitude)
      .slice(0, limit);
  }

  /**
   * Get earthquakes by location
   */
  getEarthquakesByLocation(location) {
    return this.app.state.earthquakeData.filter(eq => 
      eq.location.toLowerCase().includes(location.toLowerCase())
    );
  }

  /**
   * Calculate earthquake frequency
   */
  getEarthquakeFrequency(hours = 24) {
    const recent = this.getRecentEarthquakes(hours);
    return recent.length / hours; // earthquakes per hour
  }

  /**
   * Get magnitude distribution
   */
  getMagnitudeDistribution() {
    const data = this.app.state.earthquakeData;
    const distribution = {};

    data.forEach(eq => {
      const mag = Math.floor(eq.magnitude);
      distribution[mag] = (distribution[mag] || 0) + 1;
    });

    return distribution;
  }

  /**
   * Export statistics as JSON
   */
  exportStatistics() {
    const stats = this.getStatistics();
    const dataStr = JSON.stringify(stats, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `earthquake-stats-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  }
}

// Export for module usage
window.StatsModule = StatsModule;
