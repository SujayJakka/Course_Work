/*
 * COMP 3500: Project 5 Scheduling
 * Sujay Jakka
 * Version 1.0  11/28/2023
 *
 * This source code shows how to conduct separate compilation.
 *
 * scheduler.h: The header file of scheduler.c
 */
#ifndef _SCHEDULER_H_
#define _SCHEDULER_H_

#define MAX_TASK_NUM 32

typedef unsigned int u_int;

typedef struct task_info {
    u_int pid;
    u_int arrival_time;
    u_int burst_time;
} task_t;

void FCFS(task_t task_array[], int count);

void SRTF(task_t task_array[], int count);

void RR(task_t task_array[], int count, int quantum);

#endif
