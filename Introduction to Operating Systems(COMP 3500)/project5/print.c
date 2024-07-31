/*
 * COMP 3500: Project 5 Scheduling
 * Sujay Jakka
 * Version 1.0  11/28/2023
 *
 */


#include <stdio.h>
#include "scheduler.h"

/*
 * Print a task list. To display the task list, the length of which is specified by size.
 */
void
print_task_list(task_t task_list[], int size)
{
    int i;
    printf("There are %d tasks loaded...\n", size);
    /* print task_array to check input file */
    for (i = 0; i < size; i++)
        printf("Task PID: %u, Arrival Time: %u, Burst Time: %u\n", task_list[i].pid, \
           task_list[i].arrival_time, task_list[i].burst_time);

    printf("Press any key to continue ...\n");
    getchar();
}
