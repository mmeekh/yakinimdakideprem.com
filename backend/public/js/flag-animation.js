/**
 * Dalgalanan Türk Bayrağı Animasyonu
 * Three.js ile 3D bayrak animasyonu
 */

class FlagAnimation {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.flag = null;
        this.flagTexture = null;
        this.animationId = null;
        
        // Bayrak ayarları
        this.flagColor = "#ffffff";
        this.sizeW = 30;
        this.sizeH = 20;
        this.segW = 30;
        this.segH = 20;
        
        // Animasyon ayarları
        this.horizontal = 0.5;
        this.vertical = 0.3;
        this.swing = 0.2;
        this.speed = 0.5;
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error('Container bulunamadı:', this.containerId);
            return;
        }
        
        // Three.js scene oluştur
        this.scene = new THREE.Scene();
        
        // Kamera ayarla
        this.camera = new THREE.PerspectiveCamera(60, 400/300, 1, 1000);
        this.camera.position.set(0, 0, 40);
        this.camera.lookAt(new THREE.Vector3(0, 0, 0));
        
        // Renderer oluştur
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(400, 300);
        this.renderer.setClearColor(0xffffff); // Beyaz arka plan
        this.container.appendChild(this.renderer.domElement);
        
        // Işıklandırma
        const light = new THREE.DirectionalLight("#FFFFFF", 1);
        light.position.set(10, 50, 100);
        this.scene.add(light);
        
        const ambientLight = new THREE.AmbientLight("#999999", 0.6);
        this.scene.add(ambientLight);
        
        // Bayrak direği oluştur
        this.createPole();
        
        // Bayrak oluştur
        this.createFlag();
        
        // Türk bayrağı texture'ını yükle
        this.loadTurkishFlagTexture();
        
        // Animasyonu başlat
        this.animate();
    }
    
    createPole() {
        const geometry = new THREE.CylinderGeometry(0.5, 0.5, 40, 16, 1);
        const material = new THREE.MeshPhongMaterial({
            color: "#000000", // Siyah bayrak direği
            specular: "#333333",
            shininess: 30
        });
        const pole = new THREE.Mesh(geometry, material);
        pole.position.set(-15, -10, 0);
        this.scene.add(pole);
    }
    
    createFlag() {
        const geometry = new THREE.PlaneGeometry(this.sizeW, this.sizeH, this.segW, this.segH);
        const material = new THREE.MeshLambertMaterial({
            color: this.flagColor,
            side: THREE.DoubleSide
        });
        this.flag = new THREE.Mesh(geometry, material);
        this.scene.add(this.flag);
    }
    
    loadTurkishFlagTexture() {
        // Atatürk resmini texture olarak yükle
        const loader = new THREE.TextureLoader();
        loader.load('images/atam.jpg', (texture) => {
            texture.magFilter = THREE.LinearFilter;
            texture.minFilter = THREE.LinearFilter;
            this.flagTexture = texture;
            this.updateFlagMaterial();
        }, undefined, (error) => {
            console.log('Atatürk resmi yüklenemedi, varsayılan renk kullanılıyor:', error);
            // Hata durumunda Türk bayrağı renklerini kullan
            this.createTurkishFlagColors();
        });
    }
    
    createTurkishFlagColors() {
        // Canvas ile Türk bayrağı oluştur
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 267;
        const ctx = canvas.getContext('2d');
        
        // Kırmızı arka plan
        ctx.fillStyle = '#E30A17';
        ctx.fillRect(0, 0, 400, 267);
        
        // Beyaz hilal ve yıldız
        ctx.fillStyle = '#FFFFFF';
        
        // Hilal çizimi (basitleştirilmiş)
        ctx.beginPath();
        ctx.arc(120, 133, 50, 0, Math.PI * 2);
        ctx.fill();
        
        // Hilal içi (kırmızı)
        ctx.fillStyle = '#E30A17';
        ctx.beginPath();
        ctx.arc(130, 133, 40, 0, Math.PI * 2);
        ctx.fill();
        
        // Yıldız çizimi (basitleştirilmiş)
        ctx.fillStyle = '#FFFFFF';
        this.drawStar(ctx, 200, 100, 20, 5);
        
        // Canvas'ı texture'a çevir
        const texture = new THREE.CanvasTexture(canvas);
        texture.magFilter = THREE.LinearFilter;
        texture.minFilter = THREE.LinearFilter;
        this.flagTexture = texture;
        this.updateFlagMaterial();
    }
    
    drawStar(ctx, x, y, radius, points) {
        ctx.beginPath();
        for (let i = 0; i < points * 2; i++) {
            const angle = (i * Math.PI) / points;
            const r = i % 2 === 0 ? radius : radius * 0.5;
            const px = x + Math.cos(angle) * r;
            const py = y + Math.sin(angle) * r;
            if (i === 0) {
                ctx.moveTo(px, py);
            } else {
                ctx.lineTo(px, py);
            }
        }
        ctx.closePath();
        ctx.fill();
    }
    
    updateFlagMaterial() {
        if (this.flag) {
            this.flag.material = new THREE.MeshLambertMaterial({
                color: this.flagColor,
                map: this.flagTexture,
                side: THREE.DoubleSide
            });
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Bayrak dalgalanma animasyonu
        if (this.flag && this.flag.geometry.vertices) {
            for (let y = 0; y < this.segH + 1; y++) {
                for (let x = 0; x < this.segW + 1; x++) {
                    const index = x + y * (this.segW + 1);
                    const vertex = this.flag.geometry.vertices[index];
                    const time = Date.now() * this.speed / 50;
                    vertex.z = Math.sin(this.horizontal * x + this.vertical * y - time) * this.swing * x / 4;
                }
            }
            this.flag.geometry.verticesNeedUpdate = true;
        }
        
        this.renderer.render(this.scene, this.camera);
    }
    
    // Animasyon ayarlarını güncelle
    updateSettings(settings) {
        if (settings.horizontal !== undefined) this.horizontal = settings.horizontal;
        if (settings.vertical !== undefined) this.vertical = settings.vertical;
        if (settings.swing !== undefined) this.swing = settings.swing;
        if (settings.speed !== undefined) this.speed = settings.speed;
    }
    
    // Animasyonu durdur
    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }
    
    // Animasyonu temizle
    destroy() {
        this.stop();
        if (this.renderer) {
            this.container.removeChild(this.renderer.domElement);
            this.renderer.dispose();
        }
    }
}

// Global olarak erişilebilir yap
window.FlagAnimation = FlagAnimation;
