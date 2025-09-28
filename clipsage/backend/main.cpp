#include <QApplication>
#include <QClipboard>
#include <QMimeData>
#include <QTimer>
#include <QDir>
#include <QStandardPaths>
#include <QTextStream>
#include <QDateTime>
#include <QDebug>
#include <QImageWriter>
#include <QBuffer>
#include <QCryptographicHash>

class ClipboardManager : public QObject
{
    Q_OBJECT

public:
    explicit ClipboardManager(QObject *parent = nullptr)
        : QObject(parent)
        , m_clipboard(QApplication::clipboard())
        , m_lastText("")
        , m_lastHtml("")
        , m_counter(0)
    {
        // Create tmp directory for clipboard data
        QString tmpPath = QStandardPaths::writableLocation(QStandardPaths::TempLocation);
        m_clipboardDir = QDir(tmpPath + "/clipboard_manager");
        
        if (!m_clipboardDir.exists()) {
            m_clipboardDir.mkpath(".");
            qDebug() << "Created clipboard directory:" << m_clipboardDir.absolutePath();
        }
        
        // Connect clipboard change signal
        connect(m_clipboard, &QClipboard::dataChanged, 
                this, &ClipboardManager::onClipboardChanged);
        
        qDebug() << "Clipboard manager started. Monitoring clipboard changes...";
        qDebug() << "Saving to:" << m_clipboardDir.absolutePath();
        
        // Save initial clipboard content if any
        onClipboardChanged();
    }

private slots:
    void onClipboardChanged()
    {
        const QMimeData *mimeData = m_clipboard->mimeData();
        
        if (!mimeData || mimeData->data("application/x-qt-windows-mime").size() > 0) {
            // Skip Qt internal clipboard operations
            return;
        }
        
        QString timestamp = QDateTime::currentDateTime().toString("yyyy-MM-dd_hh-mm-ss-zzz");
        bool contentSaved = false;
        
        // Handle text data
        if (mimeData->hasText()) {
            QString text = mimeData->text();
            
            // Skip if it's the same as last text to avoid duplicates
            if (text != m_lastText && !text.isEmpty()) {
                m_counter++;
                saveTextClip(text, timestamp);
                m_lastText = text;
                contentSaved = true;
            }
        }
        
        // Only save other formats if we haven't already saved text content
        // This prevents duplicate saves for the same clipboard operation
        if (!contentSaved) {
            // Handle image data
            if (mimeData->hasImage()) {
                QImage image = qvariant_cast<QImage>(mimeData->imageData());
                if (!image.isNull()) {
                    m_counter++;
                    saveImageClip(image, timestamp);
                    contentSaved = true;
                }
            }
            
            // Handle HTML data (only if no text was saved)
            if (!contentSaved && mimeData->hasHtml()) {
                QString html = mimeData->html();
                if (!html.isEmpty() && html != m_lastHtml) {
                    m_counter++;
                    saveHtmlClip(html, timestamp);
                    m_lastHtml = html;
                    contentSaved = true;
                }
            }
            
            // Handle URLs (only if no other content was saved)
            if (!contentSaved && mimeData->hasUrls()) {
                QList<QUrl> urls = mimeData->urls();
                if (!urls.isEmpty()) {
                    m_counter++;
                    saveUrlsClip(urls, timestamp);
                    contentSaved = true;
                }
            }
        }
        
        // Only save formats info if we actually saved some content
        if (contentSaved) {
            saveFormatsInfo(mimeData, timestamp);
        }
    }

private:
    void saveTextClip(const QString &text, const QString &timestamp)
    {
        QString filename = QString("clip_%1_%2_text.txt")
                          .arg(m_counter, 6, 10, QChar('0'))
                          .arg(timestamp);
        
        QFile file(m_clipboardDir.absoluteFilePath(filename));
        if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream stream(&file);
            stream << text;
            qDebug() << "Saved text clip:" << filename << "(" << text.length() << "chars)";
        }
    }
    
    void saveImageClip(const QImage &image, const QString &timestamp)
    {
        QString filename = QString("clip_%1_%2_image.png")
                          .arg(m_counter, 6, 10, QChar('0'))
                          .arg(timestamp);
        
        QString filepath = m_clipboardDir.absoluteFilePath(filename);
        if (image.save(filepath, "PNG")) {
            qDebug() << "Saved image clip:" << filename 
                     << QString("(%1x%2)").arg(image.width()).arg(image.height());
        }
    }
    
    void saveHtmlClip(const QString &html, const QString &timestamp)
    {
        QString filename = QString("clip_%1_%2_html.html")
                          .arg(m_counter, 6, 10, QChar('0'))
                          .arg(timestamp);
        
        QFile file(m_clipboardDir.absoluteFilePath(filename));
        if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream stream(&file);
            stream << html;
            qDebug() << "Saved HTML clip:" << filename << "(" << html.length() << "chars)";
        }
    }
    
    void saveUrlsClip(const QList<QUrl> &urls, const QString &timestamp)
    {
        QString filename = QString("clip_%1_%2_urls.txt")
                          .arg(m_counter, 6, 10, QChar('0'))
                          .arg(timestamp);
        
        QFile file(m_clipboardDir.absoluteFilePath(filename));
        if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream stream(&file);
            
            for (const QUrl &url : urls) {
                stream << url.toString() << "\n";
            }
            qDebug() << "Saved URLs clip:" << filename << "(" << urls.size() << "URLs)";
        }
    }
    
    void saveFormatsInfo(const QMimeData *mimeData, const QString &timestamp)
    {
        QString filename = QString("clip_%1_%2_formats.txt")
                          .arg(m_counter, 6, 10, QChar('0'))
                          .arg(timestamp);
        
        QFile file(m_clipboardDir.absoluteFilePath(filename));
        if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream stream(&file);
            
            stream << "Clipboard Entry #" << m_counter << "\n";
            stream << "Timestamp: " << timestamp << "\n";
            stream << "Available formats:\n";
            
            QStringList formats = mimeData->formats();
            for (const QString &format : formats) {
                QByteArray data = mimeData->data(format);
                stream << "  - " << format << " (" << data.size() << " bytes)\n";
            }
            
            stream << "\nHas text: " << (mimeData->hasText() ? "Yes" : "No") << "\n";
            stream << "Has HTML: " << (mimeData->hasHtml() ? "Yes" : "No") << "\n";
            stream << "Has image: " << (mimeData->hasImage() ? "Yes" : "No") << "\n";
            stream << "Has URLs: " << (mimeData->hasUrls() ? "Yes" : "No") << "\n";
        }
    }

private:
    QClipboard *m_clipboard;
    QDir m_clipboardDir;
    QString m_lastText;
    QString m_lastHtml;
    int m_counter;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    app.setApplicationName("Simple Clipboard Manager");
    app.setApplicationVersion("1.0");
    
    // Set the platform to wayland if not already set
    if (qgetenv("QT_QPA_PLATFORM").isEmpty()) {
        qputenv("QT_QPA_PLATFORM", "wayland");
    }
    
    qDebug() << "Starting clipboard manager on platform:" << app.platformName();
    
    ClipboardManager manager;
    
    // Keep the application running
    return app.exec();
}

#include "main.moc"
