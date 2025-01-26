# Maintainer: jinx@blackzoo.de
pkgname=voll
pkgver=1.0.0
pkgrel=1
pkgdesc="V.O.L.L. - Vokabeln Ohne Langeweile Lernen"
arch=('any')
url="https://github.com/jinxblackzoo/V.O.L.L."
license=('GPL3')
depends=('python' 'gtk4' 'libadwaita' 'python-gobject' 'python-sqlalchemy' 'python-reportlab')
makedepends=('python-setuptools')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')

build() {
    cd "$pkgname-$pkgver"
    python setup.py build
}

package() {
    cd "$pkgname-$pkgver"
    python setup.py install --root="$pkgdir" --optimize=1 --skip-build

    # Desktop-Datei installieren
    install -Dm644 "desktop/voll.desktop" "$pkgdir/usr/share/applications/voll.desktop"
    
    # Icon installieren
    install -Dm644 "desktop/voll.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/voll.svg"
}
