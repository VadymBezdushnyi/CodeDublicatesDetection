#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  scanf("%d", &n);
  priority_queue<int> pq;
  for (int i = 0; i < n; i++) {
    int x;
    scanf("%d", &x);
    pq.push(x);
  }
  vector<pair<int, int> > v;
  while (!pq.empty()) {
    int x = pq.top();
    pq.pop();
    if (pq.empty()) {
      if (x % 2 == 0) {
        v.push_back({x, x / 2});
        break;
      } else {
        printf("-1");
        return 0;
      }
    }
    int y = pq.top();
    pq.pop();
    if (x != y) {
      v.push_back({x, y});
      pq.push(x - y);
    }
  }
  printf("%d\n", v.size());
  for (auto p : v) {
    printf("%d %d\n", p.first, p.second);
  }
  return 0;
}
