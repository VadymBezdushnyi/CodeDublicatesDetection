#include <bits/stdc++.h>
using namespace std;

int n;

int main() {
    cin >> n;
    multiset<int> len;
    for (int i=0, l; i<n; i++) {
        cin >> l;
        len.insert(l);
    }
    vector<pair<int,int> > ans;
    while (len.size() > 1) {
        int large = *len.rbegin();
        len.erase(prev(len.end()));
        int l2 = *len.rbegin();
        len.erase(prev(len.end()));
        if (large > l2) {
            ans.push_back({large, l2});
            len.insert(large - l2);
        }
    }
    bool minus = len.size() && ((*len.begin()) % 2 == 1);
    if (minus) {
        cout << -1 << endl;
    } else {
        cout << ans.size() + (len.size()) << "\n";
        for (auto p : ans) {
            cout << p.first << " " << p.second << "\n";
        }
        if (len.size())
            cout << (*len.begin()) << " " << (*len.begin())/2 << "\n";
    }
    
    return 0;
}
