#include "utils.cpp"
 
#define rep(i, a, b) for(int i=a; i<(b); i++)
#define rrep(i,a,b) for(int i=a; i>=b; i--)
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend()
#define pb push_back
#define popb pop_back
#define out(x) cout<<x<<endl 
#define trav(f, it)\
for(auto it = f.begin(); it != f.end(); it++)
#define fnd(f, x) (f.find(x) != f.end())
#define cfnd(f, x) (find(all(f), x) != f.end()) 

typedef long long ll;
typedef long double ld;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
typedef vector<int> vi;
typedef vector<ll> vl;
typedef vector<vi> vvi;
typedef vector<vl> vvl;
typedef vector<pii> vii;
typedef vector<pll> vll;

const float epsilon = 0.1;
const float delta_node = 1;
const int INF=1e9+7;
class point{
    public:
        float x;
        float y;
        float z;
    point(float x1, float y1, float z1){x=x1;y=y1;z=z1;}
    point(){;}

    void print()
    {
        cout<<x<<" "<<y<<" "<<z<<" ";
    }
};

int wh_len, re_len, deliv_len, nfz_len;
vector< vector<vector<float>> > nfz;
vector<point> node;
vector<vector<float>>  dist;
vector<vector<int>> edg;
vector<vector<vector<int>>> path;

//i=0 first wh_len nodes : Warehouses
//i=1 next re_len nodes : Recharge stations
//i=2 next deliv_len nodes : Delivery locations
//i=3 rest are extra nodes

int index(int i, int j)
{   
    int sum = 0;
    if(i==0) return j;
    sum += wh_len;
    if(i==1) return sum+j;
    sum += re_len;
    if(i==2) return sum+j;
    sum += deliv_len;
    if(i==3) return sum+j;
    return -INF;
}

bool liesOnLine(float x1, float y1, float z1, float x2, float y2, float z2, float x, float y, float z)
{
    float d1=sqrt((x1-x2)*(x1-x2)+ (y1-y2)*(y1-y2) + (z1-z2)*(z1-z2));
    float d2=sqrt((x1-x)*(x1-x)+ (y1-y)*(y1-y) + (z1-z)*(z1-z));
    float d3=sqrt((x-x2)*(x-x2)+ (y-y2)*(y-y2) + (z-z2)*(z-z2));
    if(abs((d2+d3-d1))<epsilon)
    {
        return true;
    }
    return false;
}
bool chkIntCuboid(point p1, point p2, vector<vector<float>> nfz)
{
    float P1[3] = {p1.x,p1.y,p1.z}, P2[3] = {p2.x,p2.y,p2.z}; 
    float center2[3], Pnum[3], Pden[3];
    for(int i=0;i<3;i++) center2[i] = nfz[0][i]+nfz[1][i];

    for(int j=0;j<2;j++)
    {
        for(int i=0;i<3;i++)
        {
            Pnum[i] = nfz[j][i];
            Pden[i] = 1;
            for(int k=0;k<3;k++)
            {
                if(k==i) continue;
                Pnum[k] = P1[k]*(P2[i]-P1[i]) + (Pnum[i]-P1[i])*(P2[k]-P1[k]);
                Pden[k] = (P2[i]-P1[i]);
            }
            int tmp = 1;
            if(P1[i]==P2[i]) tmp=0;
            if(!liesOnLine(P1[0],P1[1],P1[2],P2[0],P2[1],P2[2],((float)Pnum[0])/((float)Pden[0]),((float)Pnum[1])/((float)Pden[1]),((float)Pnum[2])/((float)Pden[2]))) tmp=0;
            for(int k=0;k<3;k++)
            {   
                if(abs(2*Pnum[k]-Pden[k]*center2[k]) > (abs(nfz[0][k]-nfz[1][k]) + 2*epsilon)*abs(Pden[k]))
                {tmp = 0;}
            }

            if(tmp==1) return true;
        }
    }

    return false;
}

void input_coordinates()
{
    wh_len = wh.size()-1; re_len = Rstations.size(); deliv_len = deliveries.size(); nfz_len = no_fly_zones.size()-1;
    int sum = 0;
    rep(i,0,wh_len)
    {
        int x1,y1,z1; 
        x1=wh[i+1].x;
        y1=wh[i+1].y;
        z1=wh[i+1].z;
        node.pb(point(x1,y1,z1));
    }

    for(auto i : Rstations)
    {
        int x1,y1,z1; 
        x1=recharge[i].location.x;
        y1=recharge[i].location.y;
        z1=recharge[i].location.z;
        node.pb(point(x1,y1,z1));
    }

    rep(i,0,deliv_len)
    {
        int x1,y1,z1; 
        x1=deliveries[i].x;
        y1=deliveries[i].y;
        z1=deliveries[i].z;
        node.pb(point(x1,y1,z1));
    }

    rep(i,0,nfz_len)
    {   
        pair<float,pair<float,float>> pt[8];
        rep(j,0,8)
        {
            int x1,y1,z1; 
            x1=no_fly_zones[i+1].vertex[j+1].x;
            y1=no_fly_zones[i+1].vertex[j+1].y;
            z1=no_fly_zones[i+1].vertex[j+1].z;
            //cin>>x1>>y1>>z1;
            pt[j] = {x1,{y1,z1}};
        }
        sort(pt,pt+8);
        vector<vector<float>> v(2,vector<float>(3));
        v[0][0] = pt[0].first;
        v[0][1] = pt[0].second.first;
        v[0][2] = pt[0].second.second;
        v[1][0] = pt[7].first;
        v[1][1] = pt[7].second.first;
        v[1][2] = pt[7].second.second;
        nfz.pb(v);
    }
}

void make_extra_nodes()
{
    for(auto cub : nfz)
    {     
        auto cube=cub;
        rep(i,0,2)
        {
            rep(j,0,3)
            {
                cube[i][j]+=(2*i-1);
            }
        }    
        rep(j,0,3)
        {
            int j1,j2;
            if(j==0){j1=1;j2=2;}
            if(j==1){j1=0;j2=2;}
            if(j==2){j1=0;j2=1;}
            rep(p,0,2)
            {
                rep(q,0,2)
                {
                    for(int d=cube[0][j]+delta_node; d<cube[1][j]; d+=delta_node)
                    {
                        int tmp[3];
                        tmp[j] = d; tmp[j1] = cube[p][j1]; tmp[j2] = cube[q][j2];
                        node.pb(point(tmp[0],tmp[1],tmp[2]));
                    }
                }
            }
        }

        rep(i,0,2)
        {
            rep(j,0,2)
            {
                rep(k,0,2) node.pb(point(cube[i][0],cube[j][1],cube[k][2]));
            }
        }
    }
}

void make_edges()
{
    rep(i,0,node.size())
    {
        vector<float> tmp(node.size(),-1);
        dist.pb(tmp);
        vector<int> v;
        edg.pb(v);
    }

    rep(i,0,node.size())
    {
        rep(j,i+1,node.size())
        {
            int tmp = 1;
            for(auto cube : nfz)
            {
                if(chkIntCuboid(node[i],node[j],cube)){tmp=0; break;}
            }
            dist[i][j] = sqrt((node[i].x-node[j].x)*(node[i].x-node[j].x) + (node[i].y-node[j].y)*(node[i].y-node[j].y) + (node[i].z-node[j].z)*(node[i].z-node[j].z));
            dist[j][i] = dist[i][j];
            if(tmp==1)
            {
                edg[i].pb(j); edg[j].pb(i); 
            }
        }
    }
}

void Djikstra_pro(int p)
{
    vector<float> dst(node.size(),INF);
    vector<int> parent(node.size(),-1);
    priority_queue<pair<float,int>,vector<pair<float,int>>,greater<pair<int,int>>> pq;
    dst[p]=0;
    pq.push({0,p});
    while(!(pq.empty()))
    {   
        auto x = pq.top();
        pq.pop();
        if(x.first != dst[x.second]) continue;
        for(auto t : edg[x.second]) 
        {
            if(dst[t]>(dst[x.second]+dist[x.second][t]))
            {
                parent[t]=x.second;
                dst[t]=dst[x.second]+dist[x.second][t];
                pq.push({dst[t],t});
            }
        }
    }
    int len = wh_len+ re_len+ deliv_len;

    rep(q,0,len)
    {
        int curr = q;
        vector<int> v;
        while(curr!=p)
        {
            if(parent[curr]==-1)
            {
                cerr<<"L lag gae in djikstra pro"<<endl;
                break;
            }
            v.pb(curr);
            curr = parent[curr];
        }
        v.pb(p);
        reverse(all(v));
        path[p][q]=v;
    }
}
void shortest_paths()
{   
    int len = wh_len+ re_len+ deliv_len;
    rep(i,0,node.size())
    {
        vvi tmp(node.size());
        path.pb(tmp);
    }
    rep(i,0,len)
    {
        Djikstra_pro(i);
    }
}

void output()
{
    int len = wh_len+ re_len+ deliv_len;
    out(wh_len); rep(i,0,wh_len){node[i].print();}
    cout<<endl;
    out(re_len); rep(i,wh_len,wh_len+re_len){node[i].print();}
    cout<<endl;
    out(deliv_len); rep(i,wh_len+re_len,len){node[i].print();}
    cout<<endl;
    rep(i,0,len)
    {
        rep(j,0,len)
        {   
            out(path[i][j].size());
            for(auto pt : path[i][j]) node[pt].print();
            cout<<endl;
        }
    }
}

pair<int,int> identify_index(int i)
{   
    int sum=0;
    if(sum<=i && i<sum+wh_len) return {0,i};
    sum += wh_len;
    if(sum<=i && i<sum+re_len) return {1,i-sum};
    sum += re_len;
    if(sum<=i && i<sum+deliv_len) return {2,i-sum};
    sum += deliv_len;
    if(sum<=i) return {3,i-sum};
    return {-1,-1};
}

int main()
{   
    #ifndef ONLINE_JUDGE
        freopen("output.txt", "w", stdout);
    #endif
    init();
    input_coordinates();
    make_extra_nodes();
    make_edges();
    shortest_paths();
    output();
    return 0;
}