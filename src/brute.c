#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define NOTIFY_FREQ 1000000
#define BOARD_SIZE 100

// macro used for debugging statements, while still exposing them to the
// compiler. be careful if using `else` nearby
#ifdef DEBUG
 #define D if(1)
#else
 #define D if(0)
#endif

// the type used to represent one tile
typedef int tile_int;

// the seed used to randomise. globally available so that functions can alert
// the user about what the seed was.
unsigned int seed;

int gcd(int a, int b) {
    int temp;
    while (b != 0) {
        temp = a % b;
        a = b;
        b = temp;
    }
    return a;
}

void gcd_merge(tile_int *arr, tile_int gcd_target,
               tile_int lower, tile_int mid, tile_int upper) {
    tile_int buffer[BOARD_SIZE];
    tile_int a, b, i;
    a = lower;
    b = mid;
    i = 0;
    D printf("merging %d:%d:%d\n", lower, mid, upper);
    while ((a < mid) && (b < upper)) {
        if (gcd(arr[a], gcd_target) > gcd(arr[b], gcd_target)) {
            buffer[i++] = arr[a++];
        } else {
            buffer[i++] = arr[b++];
        }
    }
    for (; a < mid; a++) {
        buffer[i++] = arr[a];
    }
    for (; b < upper; b++) {
        buffer[i++] = arr[b];
    }
    for (i--; i >= 0; i--) {
        arr[lower + i] = buffer[i];
    }
}

void gcd_merge_sort(tile_int *arr, tile_int gcd_target,
                    tile_int lower, tile_int upper) {
    tile_int mid;
    D printf("merge sort tgt %d, lo %d, up %d\n", gcd_target, lower, upper);
    if ((upper - lower) > 1) {
        mid = (lower + upper) / 2;
        gcd_merge_sort(arr, gcd_target, lower, mid);
        gcd_merge_sort(arr, gcd_target, mid, upper);
        gcd_merge(arr, gcd_target, lower, mid, upper);
    }
}

// fisher-yates shuffle, used to randomise the dfs
void shuffle(tile_int *arr, size_t n) {
    int i, idx;
    tile_int tmp;
    for (i = n - 1; i > 0; i--) {
        idx = rand() % (i + 1);
        tmp = arr[idx];
        arr[idx] = arr[i];
        arr[i] = tmp;
    }
}

// Get timestamp in ns - used to display processing rate
long long ns_timestamp(void) {
    struct timespec spec;
    clock_gettime(CLOCK_REALTIME, &spec);
    return 1000000000 * spec.tv_sec + spec.tv_nsec;
}

// global variable indicating program start. this is needed by functions that
// wish to determine how long the program has been running
long long PROGRAM_START;

// build a graph of integers, where each vertex indicates divisibility. this
// graph is undirected but is implemented as a two-way directed graph for DFS
// purposes
tile_int **make_graph(tile_int n) {
    // the graph is indexed from 0..n, but 0 is never used. this is to avoid
    // off-by-one errors in indexing
    tile_int **result = malloc((n + 1) * sizeof(tile_int*));
    tile_int i, j, pos;
    for (i = 1; i <= n; i++) {
        result[i] = malloc(n * sizeof(tile_int));
        pos = 0;
        for (j = 1; j < i; j++) {
            if (i % j == 0) {
                result[i][pos] = j;
                pos++;
            }
        }
        for (j = 2 * i; j <= n; j += i) {
            result[i][pos] = j;
            D printf("%d has multiple %d\n", i, j);
            pos++;
        }
        result[i][pos] = -1;
        shuffle(result[i], pos);
        gcd_merge_sort(result[i], i, 0, pos - 1);
    }
    return result;
}

// free memory from such a graph
void free_graph(tile_int **graph, tile_int size) {
    tile_int i;
    for (i = 1; i <= size; i++) {
        free(graph[i]);
    }
    free(graph);
}

// print a path
void print_path(tile_int *path, tile_int n) {
    tile_int i;
    for (i = 0; i < n; i++) {
        printf("%d ", path[i]);
    }
    putchar('\n');
}

// "callback" to analyse a path for usefulness
// tracks current best length, and depending on build conditions may also
// provide an indication of processing rate
void examine_path(tile_int *path, tile_int length) {
    static tile_int longest_path;

#ifdef DEBUG
    static long paths_seen;
    paths_seen++;
    if (paths_seen % NOTIFY_FREQ == 0) {
        printf("\r%.1e@%.1eHz: ", (double)paths_seen, (double)1000000000 * paths_seen / (ns_timestamp() - PROGRAM_START));
        fflush(stdout);
    }
#endif

    if (length > longest_path) {
        longest_path = length;
        putchar('\r');
        printf("%u[%d]", seed, length);
        print_path(path, length);
    }
}

// DFS to find paths, with extensive state parameters
// the graph of possible nodes,
// the current path, which is an array of integers up until -1, which indicates
//     the end of the path
// the length of the current path
// the end of the current path (current tile)
// the size of the board
// a boolean array tracking which vertices have been seen
void _longest_path(tile_int **graph, tile_int *path, tile_int path_length,
                   tile_int current_tile, tile_int size, bool *seen) {
    bool dead_end = true;
    tile_int i;
    tile_int nxt;
    for (nxt = graph[current_tile][i = 0];
         graph[current_tile][i] != -1;
         nxt=graph[current_tile][++i]) {
        if (!seen[nxt]) {
            dead_end = false;
            path[path_length] = nxt;
            seen[nxt] = true;
            _longest_path(graph, path, path_length + 1, nxt, size, seen);
            seen[nxt] = false;
            path[path_length] = -1;
        }
    }
    if (dead_end) {
        examine_path(path, path_length);
    }
}

// Wraps _longest_path because various parameters need to be given initial
// values, eg empty path, generate the graph, generate the "seen" array.
void longest_path(tile_int n) {
    tile_int i;
    // n + 1 as it needs to index 1..n (but we'll include 0 too)
    bool *seen = calloc(n + 1, sizeof(bool));
    // array of starting points, which we then shuffle so the DFS starts
    // randomly.
    tile_int *starting_points = malloc(n * sizeof(tile_int));
    for (i = 0; i < n; i++) {
        starting_points[i] = i + 1;
    }
    shuffle(starting_points, n);
    // initialise the path to all -1
    tile_int *path = malloc(n * sizeof(tile_int));
    for (i = 0; i < n; i++) {
        path[i] = -1;
    }
    tile_int **graph = make_graph(n);
    for (i = 0; i < n; i++) {
        path[0] = starting_points[i];
        D printf("starting point[%d] = %d\n", i, path[0]);
        seen[path[0]] = true;
        _longest_path(graph, path, 1, path[0], n, seen);
        seen[path[0]] = false;
    }
    // free for good measure. this won't ever be reached because the dfs takes
    // ludicrously long and has to be ^C'd anyway.
    D printf("freeing path\n");
    free(path);
    D printf("freeing seen\n");
    free(seen);
    D printf("freeing starting points\n");
    free(starting_points);
    D printf("freeing graph\n");
    free_graph(graph, n);
}


int main() {
    PROGRAM_START = ns_timestamp();
    seed = (unsigned int)PROGRAM_START;
    srand(seed);
    printf("seeding with %u\n", seed);
    longest_path(BOARD_SIZE);
    return 0;
}
