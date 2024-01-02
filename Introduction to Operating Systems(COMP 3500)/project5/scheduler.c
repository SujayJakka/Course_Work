/*
 * COMP 3500: Project 5 Scheduling
 * Sujay Jakka
 * Version 1.0  11/28/2023
 *
 * This source code shows how to conduct separate compilation.
 *
 * How to compile using Makefile?
 * $make
 *
 * How to manually compile?
 * $gcc -c open.c
 * $gcc -c read.c
 * $gcc -c print.c
 * $gcc open.o read.o print.o scheduler.c -o scheduler
 *
 * How to run?
 * Case 1: no argument. Sample usage is printed
 * $./scheduler
 * Usage: scheduler <file_name>
 *
 * Case 2: file doesn't exist.
 * $./scheduler file1
 * File "file1" doesn't exist. Please try again...
 *
 * Case 3: Input file
 * $./scheduler task.list
 * data in task.list is printed below...
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "scheduler.h"
#include "print.h"
#include "open.h"
#include "read.h"

int main( int argc, char *argv[] )  {
    char *file_name; /* file name from the commandline */
    FILE *fp; /* file descriptor */
    task_t task_array[MAX_TASK_NUM];

    int error_code;
    u_int i;
    u_int count;

    if (argc < 3 || argc > 4) {
        printf("Usage: scheduler task_list_file [FCFS|RR|SRTF] [time_quantum]\n");
        return EXIT_FAILURE;
    }

    error_code = open_file(argv[1], &fp);
    if (error_code == 1)
        return EXIT_FAILURE;

    read_file(fp, task_array, &count);
    print_task_list(task_array, count);
    fclose(fp);

    /* 
        Conditional statements to execute the policy that was entered.
        Includes error handling.
    
    */

    if (strcmp("FCFS", argv[2]) == 0) {
        FCFS(task_array, count);
    }

    else if (strcmp("SRTF", argv[2]) == 0) {
        SRTF(task_array, count);
    }

    else if(strcmp("RR", argv[2]) == 0) {
        if (argc == 4) {
            int quantum = atoi(argv[3]);
            RR(task_array, count, quantum);
        }
        else {
            printf("Please enter the time quantum parameter for the RR policy.\n");
            return EXIT_FAILURE;
        }
    }

    else {
        printf("Please enter a valid scheduling policy.\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}

void FCFS(task_t task_array[], int count) {

    int time = 0;
    int finished_tasks = 0;
    int ready_queue_count = 0;
    int wasted_cycles = 0;

    // Waiting time and response time are the same in FCFS
    int overall_waiting = 0;
    int overall_turn_around_time = 0;

    task_t ready_queue[count];

    printf("==================================================================\n");

    while (finished_tasks != count) {

        // Add new processes to the queue
        for (int i = 0; i < count; i++) {
            task_t possible_new_task = task_array[i];
            if (possible_new_task.arrival_time == time) {
                ready_queue[ready_queue_count] = possible_new_task;
                ready_queue_count++;
            }
        }

        // If there is no process to run at the moment continue to the next iteration/time unit

        if (ready_queue_count == 0) {
            printf("<time %d> idle\n", time);
            wasted_cycles++;
            time++;
            continue;
        }

        task_t *current_task = &ready_queue[0];

        // Run Process
        printf("<time %d> process %u is running\n", time, current_task->pid);
        current_task->burst_time--;
        time++;

        // Increment waiting time for other processes
        overall_waiting += (ready_queue_count - 1);

        // Remove finished process from queue
        if (current_task->burst_time == 0) {
            printf("<time %d> process %u is finished...\n", time, current_task->pid);
            overall_turn_around_time += (time - current_task->arrival_time);
            finished_tasks++;

            for (int i = 1; i < ready_queue_count; i++) {
                ready_queue[i - 1] = ready_queue[i];
            }

            ready_queue_count--;

        }

    }

    // Print out statistic on waiting time, response time, turnaround time, and CPU usage

    float average_waiting_time = (float)overall_waiting / count;
    float average_turn_around_time = (float)overall_turn_around_time / count;
    float cpu_usage = (((float)time - wasted_cycles) / time) * 100;

    printf("<time %d> All processes finished ......\n", time);
    printf("==================================================================\n");
    printf("Average waiting time: %.2f\n", average_waiting_time);
    printf("Average response time: %.2f\n", average_waiting_time);
    printf("Average turnaround time: %.2f\n", average_turn_around_time);
    printf("Overall CPU usage: %.2f%%\n", cpu_usage);
    printf("==================================================================\n");

}


void SRTF(task_t task_array[], int count) {

    int time = 0;
    int finished_tasks = 0;

    // Variable to keep track of processes that responded
    int responded_processes = 0;
    int ready_queue_count = 0;
    int wasted_cycles = 0;

    int overall_waiting = 0;

    // Added an overall response time variable as response time does not equal waiting time in SRTF
    int overall_response_time = 0;
    int overall_turn_around_time = 0;

    // Added array of responded processes
    int responded_array[count];

    task_t ready_queue[count];

    printf("==================================================================\n");

    while (finished_tasks != count) {

        // Add new processes to the queue
        for (int i = 0; i < count; i++) {
            task_t possible_new_task = task_array[i];
            if (possible_new_task.arrival_time == time) {
                ready_queue[ready_queue_count] = possible_new_task;
                ready_queue_count++;
            }
        }

        // If there is no process to run at the moment continue to the next iteration/time unit
        if (ready_queue_count == 0) {
            printf("<time %d> idle\n", time);
            wasted_cycles++;
            time++;
            continue;
        }

        // Select process with the shortest remaining time
        task_t *current_task = &ready_queue[0];
        int current_task_index = 0;

        for (int i = 1; i < ready_queue_count; i++) {
            if (current_task->burst_time > ready_queue[i].burst_time) {
                current_task = &ready_queue[i];
                current_task_index = i;
            }
        }

        // Checks to see if this task has already responded
        int responded = 0;

        for (int i = 0; i < responded_processes; i++) {
            if (current_task->pid == responded_array[i]) {
                responded = 1;
                break;
            }
        }

        // If task has not responded yet add it to the responded array
        if (responded == 0) {
            responded_array[responded_processes] = current_task->pid;
            responded_processes++;
        }

        // Run process
        printf("<time %d> process %u is running\n", time, current_task->pid);
        current_task->burst_time--;
        time++;

        // Increment waiting time for other processes
        overall_waiting += (ready_queue_count - 1);

        // Increment response time for other processes
        overall_response_time += (ready_queue_count - (responded_processes - finished_tasks));

        // Remove finished process from queue
        if (current_task->burst_time == 0) {
            printf("<time %d> process %u is finished...\n", time, current_task->pid);
            overall_turn_around_time += (time - current_task->arrival_time);
            finished_tasks++;

            for (int i = current_task_index + 1; i < ready_queue_count; i++) {
                ready_queue[i - 1] = ready_queue[i];
            }

            ready_queue_count--;

        }

    }

    // Print out statistic on waiting time, response time, turnaround time, and CPU usage

    float average_waiting_time = (float)overall_waiting / count;
    float average_response_time = (float)overall_response_time / count;
    float average_turn_around_time = (float)overall_turn_around_time / count;
    float cpu_usage = (((float)time - wasted_cycles) / time) * 100;

    printf("<time %d> All processes finished ......\n", time);
    printf("==================================================================\n");
    printf("Average waiting time: %.2f\n", average_waiting_time);
    printf("Average response time: %.2f\n", average_response_time);
    printf("Average turnaround time: %.2f\n", average_turn_around_time);
    printf("Overall CPU usage: %.2f%%\n", cpu_usage);
    printf("==================================================================\n");

}

void RR(task_t task_array[], int count, int quantum) {

    int time = 0;
    int finished_tasks = 0;

    // Variable to keep track of processes that responded
    int responded_processes = 0;
    int ready_queue_count = 0;
    int wasted_cycles = 0;

    // Variable that shows how much time a process has until it needs to be switched
    int time_until_switch = quantum;

    int overall_waiting = 0;
    int overall_response_time = 0;
    int overall_turn_around_time = 0;


    // Added array of responded processes
    int responded_array[count];

    task_t ready_queue[count];

    printf("==================================================================\n");

    while (finished_tasks != count) {

        // Add new processes to the queue
        for (int i = 0; i < count; i++) {
            task_t possible_new_task = task_array[i];
            if (possible_new_task.arrival_time == time) {
                ready_queue[ready_queue_count] = possible_new_task;
                ready_queue_count++;
            }
        }

        // If there is no process to run at the moment continue to the next iteration/time unit
        if (ready_queue_count == 0) {
            printf("<time %d> idle\n", time);
            wasted_cycles++;
            time++;
            continue;
        }

        // Select the process that needs to b executed for this Round Robin quantum iteration
        task_t *current_task = &ready_queue[0];

        // Checks to see if this task has already responded
        int responded = 0;

        for (int i = 0; i < responded_processes; i++) {
            if (current_task->pid == responded_array[i]) {
                responded = 1;
                break;
            }
        }

        // If task has not responded yet add it to the responded array
        if (responded == 0) {
            responded_array[responded_processes] = current_task->pid;
            responded_processes++;
        }

        // Run process
        printf("<time %d> process %u is running\n", time, current_task->pid);
        current_task->burst_time--;
        time++;
        time_until_switch--;

        // Increment waiting time for other processes
        overall_waiting += (ready_queue_count - 1);

        // Increment response time for other processes
        overall_response_time += (ready_queue_count - (responded_processes - finished_tasks));

        // Remove finished process from queue
        if (current_task->burst_time == 0) {
            printf("<time %d> process %u is finished...\n", time, current_task->pid);
            overall_turn_around_time += (time - current_task->arrival_time);
            finished_tasks++;

            for (int i = 1; i < ready_queue_count; i++) {
                ready_queue[i - 1] = ready_queue[i];
            }

            ready_queue_count--;
            time_until_switch = quantum;

        }

        /* 
            Process is not done but its quantum time has expired.
            Switch to another process.
        */

        else if(time_until_switch == 0) {

            task_t current_task = ready_queue[0];

            for (int i = 1; i < ready_queue_count; i++) {
                ready_queue[i - 1] = ready_queue[i];
            }

            ready_queue[ready_queue_count - 1] = current_task;

            time_until_switch = quantum;
            
        }

    }

    // Print out statistic on waiting time, response time, turnaround time, and CPU usage

    float average_waiting_time = (float)overall_waiting / count;
    float average_response_time = (float)overall_response_time / count;
    float average_turn_around_time = (float)overall_turn_around_time / count;
    float cpu_usage = (((float)time - wasted_cycles) / time) * 100;

    printf("<time %d> All processes finished ......\n", time);
    printf("==================================================================\n");
    printf("Average waiting time: %.2f\n", average_waiting_time);
    printf("Average response time: %.2f\n", average_response_time);
    printf("Average turnaround time: %.2f\n", average_turn_around_time);
    printf("Overall CPU usage: %.2f%%\n", cpu_usage);
    printf("==================================================================\n");

}
