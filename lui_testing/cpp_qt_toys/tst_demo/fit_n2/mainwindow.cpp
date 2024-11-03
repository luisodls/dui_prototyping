#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <iostream>
#include <QFileDialog>
#include <QString>


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_ini_clicked()
{
    QString  file1Name ;
    file1Name = QFileDialog::getOpenFileName(this,
             tr("Open File 1"), "/home", tr("all Files (*.*)"));
        ui->GraphPath->setText(file1Name);

}

void MainWindow::on_pushButton_run_clicked()
{
    std::cout << "Hello from pushButton_run " << std::endl;
}

