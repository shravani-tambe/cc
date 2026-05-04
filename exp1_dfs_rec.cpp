#include<iostream> 
#include <vector> 
#include <stack> 
using namespace std;

void printStack(stack<int> st) 
{ 
cout << "Stack (top -> bottom): "; 
while (!st.empty()) {
cout << st.top() << " "; st.pop();
}
cout << endl;
}
void DFS_non_recursive(vector< vector<int> > &graph, int start) 
{ 
vector<bool> visited(graph.size(), false);
vector<int> traversal; stack<int> st; st.push(start);
cout << "\n--- DFS (Non-Recursive) Step-by-Step ---\n"; 
int step = 0;
while (!st.empty()) {
cout << "\nStep " << ++step << ":\n"; printStack(st);
int node = st.top(); st.pop();
cout << "Popped node: " << node << endl; 
if (!visited[node]) {
visited[node] = true; traversal.push_back(node);
cout << "Visited node: " << node << endl;
// Push neighbors in reverse order
for (int i = graph[node].size() - 1; i >= 0; i--) 
{ int neighbor = graph[node][i];
if (!visited[neighbor]) { st.push(neighbor);
cout << "Pushed " << neighbor << " into stack\n";
} else {
cout << "Node " << neighbor << " already visited\n";
}
}
} else {
cout << "Node " << node << " already visited, skipping\n";
}
 
}
cout << "\n--- Traversal Complete ---\n";
// ?? Final Traversal
cout << "\nFinal DFS Traversal Path: "; 
for (int i = 0; i < traversal.size(); i++) {
cout << traversal[i] << " ";
}
cout << endl;
// Complexity
int V = graph.size(); int E = 0;
for (int i = 0; i < V; i++) { E += graph[i].size();
}
E /= 2;
cout << "\nTime Complexity: O(b^d)\n"; cout << "Space Complexity: O(d)\n";
}

int main() { int V, E;
cout << "Enter number of vertices: "; cin >> V;
if (V <= 0) {
cout << "Invalid vertices!\n"; return 0;
}
vector< vector<int> > graph(V); 
cout << "Enter number of edges: "; cin >> E;
cout << "Enter edges (0 to " << V-1 << "):\n"; for (int i = 0; i < E; i++) {
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
DFS_non_recursive(graph, start); return 0;
}
