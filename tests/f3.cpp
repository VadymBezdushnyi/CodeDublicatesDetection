#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/detail/standard_policies.hpp>
using ll = int64_t;
using ld = long double;
using ull = uint64_t;
using namespace std;

int main() {
    freopen("input.txt", "r", stdin); freopen("output.txt", "w", stdout);
    ios_base::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); cout.setf(ios::fixed); cout.precision(20); 
    int n, l;
    cin >> n >> l;
    int cur = 0, sm = 0;
    for (int i = 0; i < n; ++i) {
        int f, w;
        cin >> f >> w;
        if (f) {
            if ((sm += w) >= l) {
                cout << cur + 1 << "\n";
                return 0;
            }
        } else {
            cur = i + 1;
            sm = 0;
        }
    }

    cout << -1 << "\n";
}
