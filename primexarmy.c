#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

typedef struct {
    char ip[64];
    int port;
    char method[16];
    int duration;
} Task;

void *task_worker(void *arg) {
    Task *t = (Task*)arg;
    time_t start = time(NULL);

    while (time(NULL) - start < t->duration) {
        printf("[PRIMEXARMY] Simulating %s traffic -> %s:%d (elapsed %lds)\n",
               t->method, t->ip, t->port, time(NULL) - start);
        fflush(stdout);
        usleep(500000); // 0.5s delay
    }

    printf("[PRIMEXARMY] Simulation finished for %s:%d (%s)\n",
           t->ip, t->port, t->method);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        printf("Usage: %s <ip> <port> <method> <time>\n", argv[0]);
        return 1;
    }

    Task t;
    strncpy(t.ip, argv[1], sizeof(t.ip)-1);
    t.port = atoi(argv[2]);
    strncpy(t.method, argv[3], sizeof(t.method)-1);
    t.duration = atoi(argv[4]);

    printf("🚀 PRIMEXARMY Simulation Started\n");
    printf("Target: %s:%d\nMethod: %s\nDuration: %d sec\n\n",
           t.ip, t.port, t.method, t.duration);

    pthread_t th;
    pthread_create(&th, NULL, task_worker, &t);
    pthread_join(th, NULL);

    printf("✅ PRIMEXARMY Simulation Complete\n");
    return 0;
}
