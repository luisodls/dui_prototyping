#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE
class a_scene : public QGraphicsScene
{
    Q_OBJECT
public slots:
    void mouseMoveEvent(QGraphicsSceneMouseEvent *event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override;
    void clear_n_rect();

signals:
    void vectorChanged(double proy_x, double proy_y);
    void time2fire();
};

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void update_texts(double proy_x, double proy_y);
    void UpdateDrawing();

public slots:
    void on_RunButton_clicked();
    void on_EditEntryX_textChanged(const QString &arg1);
    void on_EditEntryY_textChanged(const QString &arg1);

public:
    Ui::MainWindow *ui;
    double inX, inY, vx, vy, x_pos, y_pos, prev_x, prev_y;
    bool flying = false;

    a_scene *my_scene;
};

#endif // MAINWINDOW_H
