#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "iostream"
#include <QGraphicsSceneMouseEvent>
#include <math.h>
#include <QTimer>

void a_scene::mouseMoveEvent(QGraphicsSceneMouseEvent* event)
{
    QPointF NewPos = event->scenePos();
    double x, y, proy_x, proy_y;
    x = NewPos.x();
    y = NewPos.y();

    this->clear_n_rect();
    this->addLine(0, 0, x, y);
    proy_x = double(-x) * 0.05;
    proy_y = double(-y) * 0.05;
    emit vectorChanged(proy_x, proy_y);
}
void a_scene::clear_n_rect()
{
    this->clear();
    this->addRect(QRect(0, 0, 400, 300));
}
void a_scene::mouseReleaseEvent(QGraphicsSceneMouseEvent* event)
{
    std::cout << "mouseReleaseEvent at: "
              << event->scenePos().x() << ", " << event->scenePos().y()
              << std::endl;
    std::cout << "fire: " << std::endl;
    emit time2fire();
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    my_scene = new a_scene();

    ui->gView->setScene(my_scene);
    my_scene->setSceneRect(0, 0, 400, 300);
    ui->gView->scale(1, -1);
    my_scene->clear_n_rect();

    QObject::connect(
        my_scene, &a_scene::vectorChanged,
        this, &MainWindow::update_texts
    );


    QObject::connect(
        my_scene, &a_scene::time2fire,
        this, &MainWindow::launch_now
    );
    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &MainWindow::UpdateDrawing);
    timer->start(10);
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::UpdateDrawing(){
    double x_pr, y_pr, l;

    if (flying == true) {
        if (x_pos < my_scene->width() and y_pos > 0) {
            x_pos += vx;
            y_pos += vy;
            my_scene->clear_n_rect();
            l = sqrt(vx * vx + vy * vy);
            x_pr = (vx / l) * 25;
            y_pr = (vy / l) * 25;
            my_scene->addLine(int(x_pos), int(y_pos), int(prev_x - x_pr), int(prev_y - y_pr));
            vx = vx * 0.998;
            vy = vy * 0.998;
            vy -= 0.01;
            prev_x = x_pos;
            prev_y = y_pos;
        } else {
            flying = false;
        }
    }
}
void MainWindow::update_texts(double proy_x, double proy_y)
{
    std::cout << "time to update texts to ( " << proy_x << ", " << proy_y << " )" << std::endl;
    QString str_x = QString::number(proy_x);
    QString str_y = QString::number(proy_y);
    ui->EditEntryX->setText(str_x);
    ui->EditEntryY->setText(str_y);
}
void MainWindow::launch_now()
{
    std::cout << "Time to shoot with vector:  " << inX << ", " << inY << std::endl;
    my_scene->addLine(0, 0, int(inX), int(inY));

    vx = inX;
    vy = inY;
    y_pos = 0.01;
    x_pos = 0.01;
    prev_x = 0;
    prev_y = 0;
    flying = true;
}
void MainWindow::on_EditEntryX_textChanged(const QString &arg1)
{
    inX = arg1.toDouble();
    std::cout << "typed:" << inX << std::endl;
}
void MainWindow::on_EditEntryY_textChanged(const QString &arg1)
{
    inY = arg1.toDouble();
    std::cout << "typed:" << inY << std::endl;
}

