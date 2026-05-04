#include <iostream> #include <vector> using namespace std;

void DFS(vector< vector<int> > &graph, int node, vector<bool> &visited, vector<int> &traversal, int &step) {
cout << "\nStep " << ++step << ":\n";
cout << "Visiting node: " << node << endl; visited[node] = true; traversal.push_back(node);
for (int i = 0; i < graph[node].size(); i++) { int neighbor = graph[node][i];
if (!visited[neighbor]) {
cout << "Going deeper to node: " << neighbor << endl; DFS(graph, neighbor, visited, traversal, step);
} else {
cout << "Node " << neighbor << " already visited\n";
}
}
cout << "Backtracking from node: " << node << endl;
}

int main() { int V, E;
cout << "Enter number of vertices: "; cin >> V;
vector< vector<int> > graph(V); cout << "Enter number of edges: "; cin >> E;
cout << "Enter edges (u v):\n"; for (int i = 0; i < E; i++) {
int u, v;
cin >> u >> v; graph[u].push_back(v); graph[v].push_back(u);
}
int start;
cout << "Enter starting vertex: "; cin >> start;
vector<bool> visited(V, false); vector<int> traversal;
int step = 0;
cout << "\n--- DFS Step-by-Step Traversal ---\n";
 
DFS(graph, start, visited, traversal, step); cout << "\n--- Traversal Complete ---\n";

// ?? FINAL OUTPUT
cout << "\nFinal DFS Traversal Path: "; for (int i = 0; i < traversal.size(); i++) {
cout << traversal[i] << " ";
}
cout << endl;
// Complexity int Ecount = 0;
for (int i = 0; i < V; i++) { Ecount += graph[i].size();
}
Ecount /= 2;
cout << "\nTime Complexity: O(b^d)\n"; cout << "Space Complexity: O(d)\n"; return 0;
