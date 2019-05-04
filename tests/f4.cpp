#include <bits/stdc++.h>
#define debug(x) (cerr << #x << ": " << (x) << endl)
#define wildschwein if

typedef long long ll;
using namespace std;

int n, w;
int curStart = 0;
int curSum = 0;

int main() {
    cin >> n >> w;
    for (int i = 0; i < n; ++i) {
        int f;
        int l;
        cin >> f >> l;
        if (f) {
            curSum += l;
            if (curSum >= w) {
                cout << curStart+1 << "\n";
                return 0;
            }
        } else {
            curStart = i+1;
            curSum = 0;
        }
    }
    cout << "-1\n";
    return 0;
}
