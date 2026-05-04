#include <iostream> 
#include <vector> 
#include <queue> 
using namespace std;

void printQueue(queue<int> q) 
{ cout << "Queue: ";
while (!q.empty()) {
cout << q.front() << " "; q.pop();
}
cout << endl;
}

void BFS_recursive(vector< vector<int> > &graph, queue<int> &q, vector<bool> &visited, vector<int> &traversal, int &step) {

if (q.empty()) return;

cout << "\nStep " << ++step << ":\n"; printQueue(q);

int node = q.front(); q.pop();

cout << "Processing node: " << node << endl; traversal.push_back(node);
for (int i = 0; i < graph[node].size(); i++) { int neighbor = graph[node][i];

if (!visited[neighbor]) { visited[neighbor] = true; q.push(neighbor);
cout << "Visited " << neighbor << " and added to queue\n";
} else {
cout << "Node " << neighbor << " already visited\n";
}
}

// Recursive call
 
BFS_recursive(graph, q, visited, traversal, step);
}

int main() { int V, E;

cout << "Enter number of vertices: "; cin >> V;

vector< vector<int> > graph(V);

cout << "Enter number of edges: "; cin >> E;

cout << "Enter edges (u v):\n"; for (int i = 0; i < E; i++) {
int u, v;
cin >> u >> v;

if (u < 0 || u >= V || v < 0 || v >= V) { cout << "Invalid edge! Try again\n"; i--;
continue;
}

graph[u].push_back(v); graph[v].push_back(u);
}

int start;
cout << "Enter starting vertex: "; cin >> start;

if (start < 0 || start >= V) {
cout << "Invalid start node!\n"; return 0;
}

vector<bool> visited(V, false); vector<int> traversal; queue<int> q;
int step = 0; visited[start] = true;
 
q.push(start);

cout << "\n--- BFS (Recursive) Step-by-Step ---\n";
BFS_recursive(graph, q, visited, traversal, step); cout << "\n--- Traversal Complete ---\n";
// ?? Final Traversal
cout << "\nFinal BFS Traversal Path: "; for (int i = 0; i < traversal.size(); i++) {
cout << traversal[i] << " ";
}
cout << endl;

// Complexity
int Vcount = graph.size(); int Ecount = 0;
for (int i = 0; i < Vcount; i++) 
{ Ecount += graph[i].size();
}
Ecount /= 2;
cout << "\nTime Complexity: O(b^d)\n"; cout << "Space Complexity: O(b^d)\n";

return 0;
}
