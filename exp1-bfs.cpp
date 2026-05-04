#include <iostream>
#include <vector>
#include <queue>
using namespace std;

// Function to print queue (for visualization)
void printQueue(queue<int> q) {
    cout << "Queue: ";
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
}

// BFS function
void BFS(vector<vector<int>> &graph, int start) {
    vector<bool> visited(graph.size(), false);
    vector<int> traversal;
    queue<int> q;

    visited[start] = true;
    q.push(start);

    cout << "\n--- BFS Step-by-Step Traversal ---\n";
    int step = 0;

    while (!q.empty()) {
        cout << "\nStep " << ++step << ":\n";
        printQueue(q);

        int node = q.front();
        q.pop();

        cout << "Processing node: " << node << endl;
        traversal.push_back(node);

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
                cout << "Visited " << neighbor << " and added to queue\n";
            }
        }
    }

    cout << "\n--- Traversal Complete ---\n";

    // Final traversal output
    cout << "\nFinal BFS Traversal Path: ";
    for (int node : traversal) {
        cout << node << " ";
    }
    cout << endl;

    // Complexity
    cout << "Time Complexity: O(V + E)\n";
    cout << "Space Complexity: O(V)\n";
}

// Main function
int main() {
    int V, E;

    cout << "Enter number of vertices: ";
    cin >> V;

    vector<vector<int>> graph(V);

    cout << "Enter number of edges: ";
    cin >> E;

    cout << "Enter edges (0 to " << V - 1 << "):\n";
    for (int i = 0; i < E; i++) {
        int u, v;
        cin >> u >> v;

        if (u < 0 || u >= V || v < 0 || v >= V) {
            cout << "Invalid edge! Try again.\n";
            i--;
            continue;
        }

        graph[u].push_back(v);
        graph[v].push_back(u); // undirected graph
    }

    int start;
    cout << "Enter starting vertex: ";
    cin >> start;

    if (start < 0 || start >= V) {
        cout << "Invalid starting vertex!\n";
        return 0;
    }

    BFS(graph, start);

    return 0;
}