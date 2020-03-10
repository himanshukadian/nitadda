#include<iostream>
#include<vector>
#include<map>
#include<set>
#include<algorithm>
#include<cstring>
#include<map>
#include<iomanip>
#define ll long long int
#define faster ios_base::sync_with_stdio(false),cin.tie(NULL),cout.tie(NULL);
using namespace std;
bool Check(pair<int, pair<ll,ll> > a,pair<int, pair<ll,ll> > b){
	return a.second.second<b.second.second;
}
int main(){
	int t;cin>>t;
	while(t--){
		ll n;cin>>n;
		ll a[n],b[n];
		for(int i=0;i<n;i++)cin>>a[i];
		for(int i=0;i<n;i++)cin>>b[i];
		vector< pair<int, pair<ll,ll> > >v;
		for(int i=0;i<n;i++){
			v.push_back(make_pair(i+1,make_pair(a[i],b[i])));
		}
        sort(v.begin(),v.end(),Check);
        //ll cnt=1;
        int j=0;
        cout<<v[0].first<<" ";
        for(int i=1;i<n;i++){
        	if(v[j].second.second<=v[i].second.first){
        		j=i;
        		cout<<v[i].first<<" ";
        	}
        }
        cout<<endl;
	}
	return 0;
}