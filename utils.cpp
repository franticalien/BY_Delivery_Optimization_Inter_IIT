#include <bits/stdc++.h>
using namespace std;

/* **************************
 * Contains implementations of classes of 
 * Item, Delivery, Drone, Location + Cube, Recharge Station
 * and some functions to read input by default from "Parameters.csv" and "Demands.csv"
 * The default values of some parameters of drones, warehouses, etc. have been hardcoded 
 * (which are explicitly mentioned to be constant across all complexities and input test cases)
 ? The attributes have been made public so that they can be accessed from everywhere, and the vectors 
 ? of Drone, WH, Recharge Stations, etc., have been made global variables so that they can be accessed from anywhere too
 * To use this file in some other file, simply write 
 * `#include "utils.cpp" at the top, and write `init()` in the beginning of `main()`
 * to read input and initialize default variables.
************************** */

class Item{
    public:
        int type, wt, l, b, h, vol;
        Item(int W, int L, int B, int H, int t){
            wt=W, l=L, b=B, h=H, type=t;
            vol = L*B*H;
        }
        Item(){;}
};
vector<Item> item_params(6);
void init_item_params(){
    {Item i{1,5,8,5,1}; item_params[1]=i;}
    {Item i{6,5,10,8,2}; item_params[2]=i;}
    {Item i{4,5,10,15,3}; item_params[3]=i;}
    {Item i{2,15,10,8,4}; item_params[4]=i;}
    {Item i{5,20,15,10,5}; item_params[5]=i;}
}

class Delivery{
    public:
        string id, from, to;
        Item item;
        bool failure;
        int wh, day, x, y, z;
        void print_delivery(){ // * For debugging/verification
            cout<<"WH:"<<wh<<"\t"<<"ID:"<<id<<"\t"<<"Item:"<<item.type<<"\t"<<"Day:"<<day<<"\t"<<"X:"<<x<<"\t"<<"Y:"<<y<<"\t"<<"Z:"<<z<<"\t"<<"From:"<<from<<"\t"<<"To:"<<to<<"\t"<<"Failure:"<<failure<<"\n";
        }
};
vector<Delivery> inp_deliveries(string filename="input/Demand.csv"){
    fstream fin(filename, ios::in);
    fin.is_open();
    vector<Delivery> deliveries;

    string line, temp, X, Y, Z;
    getline(fin, line);
    while(getline(fin, line)){
        stringstream s(line);
        Delivery d;

        getline(s, temp, ',');  d.wh = temp[2]-'0';
        getline(s, d.id, ',');
        getline(s, temp, ',');  d.item = item_params[temp[5]-'0'];
        getline(s, temp, ',');  d.day = temp[4]-'0';
        getline(s, X, ',');     d.x = stoi(X);
        getline(s, Y, ',');     d.y = stoi(Y);
        getline(s, Z, ',');     d.z = stoi(Z);
        getline(s, d.from, ',');
        getline(s, d.to, ',');
        getline(s, temp, ',');  d.failure = temp[0]-'0';

        deliveries.push_back(d);
    }

    return deliveries;
}

class Drone{
    public:
        int battery, payload_cap, payload_cap_vol, slots, count;
        int maintenance_fixed, maintenance_var;
        float base_wt, a, b, c, p, q;
        Drone(){;}
        Drone(int b, float w, int pc, int pcv, int s, int mf, int mv){
            battery=b, base_wt=w, payload_cap=pc, payload_cap_vol=pcv, slots=s, maintenance_fixed=mf, maintenance_var=mv;
        }
        void print_drone(){// * For debugging/verification
            cout<<"Battery:"<<battery<<"\t"<<"Cap:"<<payload_cap<<"\t"<<"Vol:"<<payload_cap_vol<<"\t"<<"Slots:"<<slots<<"\t"<<"Count:"<<count<<"\t"<<"Cost:"<<maintenance_fixed<<"\t"<<"Cost:"<<maintenance_var<<"\t"<<"Wt:"<<base_wt<<"\t"<<"A:"<<a<<"\t"<<"B:"<<b<<"\t"<<"C:"<<c<<"\t"<<"P:"<<p<<"\t"<<"Q:"<<q<<"\n";
        }
};
vector<Drone> drone_params(7);
void init_drone_params(){
{Drone d(2000, 2, 5, 200, 1, 10, 5); drone_params[1]=d;}
{Drone d(2500, 2.5, 6, 500, 1, 15, 8); drone_params[2]=d;}
{Drone d(3000, 3, 7, 1000, 2, 20, 13); drone_params[3]=d;}
{Drone d(4000, 3.5, 8, 2000, 2, 20, 15); drone_params[4]=d;}
{Drone d(5000, 4, 9, 3000, 2, 30, 20); drone_params[5]=d;}
{Drone d(10000, 5, 10, 5000, 4, 50, 25); drone_params[6]=d;}
}

class Location{
    public:
    int x=INT_MIN, y=INT_MIN, z=0;
    Location(int X, int Y, int Z){x=X,y=Y,z=Z;}
    Location(){;}
};
class cube{
    public:
        vector<Location> vertex;
        cube(){vertex.resize(9);}
};
vector<cube> no_fly_zones(1);

int max_speed;
float cost_per_energy;
vector<int> Rstations;
vector<Location> wh(2);
vector<Location> w;
vector<Delivery> deliveries;

class Recharge_Station{
    public:
        int slots, current; Location location;
        Recharge_Station(int s, int c){
            slots=s, current=c;
        }
        Recharge_Station(){;}
};
vector<Recharge_Station> recharge(6);
void init_recharge_params(){
    {Recharge_Station r(1,3); recharge[1] = r;}
    {Recharge_Station r(1,3); recharge[2] = r;}
    {Recharge_Station r(1,3); recharge[3] = r;}
    {Recharge_Station r(4,3); recharge[4] = r;}
    {Recharge_Station r(5,3); recharge[5] = r;}
}

void inp_parameters(string filename="input/Parameters.csv"){
    fstream fin(filename, ios::in);
    fin.is_open();
    wh[1] = Location(0, 0, 0);

    string line, cell, temp;
    getline(fin, line);
    while(getline(fin, line)){
        stringstream s(line);
        
        getline(s, cell, ',');
        if(line.find("MaxSpeed") != string::npos){
            getline(s, cell, ',');
            max_speed = stoi(cell);
        }else if(line.find("Cost") != string::npos){
            getline(s, cell, ',');
            cost_per_energy = stof(cell);
        }else if(line.find("Noflyzone") != string::npos && cell[0]=='X'){
            int i = (cell[2]=='0' ? 10 : cell[1]-'0');
            if(i+1>no_fly_zones.size()){
                no_fly_zones.resize(i+1);
            }
            int j = (cell[2]=='0' ? cell[3]-'0' : cell[2]-'0');
            getline(s, cell, ',');
            no_fly_zones[i].vertex[j].x = stoi(cell);
        }else if(line.find("Noflyzone") != string::npos && cell[0]=='Y'){
            int i = (cell[2]=='0' ? 10 : cell[1]-'0');
            int j = (cell[2]=='0' ? cell[3]-'0' : cell[2]-'0');
            getline(s, cell, ',');
            no_fly_zones[i].vertex[j].y = stoi(cell);
        }else if(line.find("Noflyzone") != string::npos && cell[0]=='Z'){
            int i = (cell[2]=='0' ? 10 : cell[1]-'0');
            int j = (cell[2]=='0' ? cell[3]-'0' : cell[2]-'0');
            getline(s, cell, ',');
            no_fly_zones[i].vertex[j].z = stoi(cell);
        }else if(line.find("WH Location") != string::npos && cell[3]=='X'){
            if(cell[2]-'0'+1>wh.size()){
                wh.resize(cell[2]-'0'+1);
            }
            int i=cell[2]-'0';
            getline(s, cell, ',');
            wh[i].x = stoi(cell);
        }else if(line.find("WH Location") != string::npos && cell[3]=='Y'){
            if(cell[2]-'0'+1>wh.size()){
                wh.resize(cell[2]-'0'+1);
            }
            int i=cell[2]-'0';
            getline(s, cell, ',');
            wh[i].y = stoi(cell);
        }else if(line.find("WH Location") != string::npos && cell[3]=='Z'){
            if(cell[2]-'0'+1>wh.size()){
                wh.resize(cell[2]-'0'+1);
            }
            int i=cell[2]-'0';
            getline(s, cell, ',');
            wh[i].z = stoi(cell);
        }else if(line.find("Recharge") != string::npos && cell[1]=='X'){
            int i=cell[0]-'A'+1;
            Rstations.push_back(i);
            getline(s, cell, ',');
            recharge[i].location.x = stoi(cell);
        }else if(line.find("Recharge") != string::npos && cell[1]=='Y'){
            int i=cell[0]-'A'+1;
            getline(s, cell, ',');
            recharge[i].location.y = stoi(cell);
        }else if(line.find("Drone") != string::npos && cell[0] == 'P'){
            int i = cell[1]-'0';
            getline(s, cell, ',');
            drone_params[i].p = stof(cell);
        }else if(line.find("Drone") != string::npos && cell[0] == 'Q'){
            int i = cell[1]-'0';
            getline(s, cell, ',');
            drone_params[i].q = stof(cell);
        }else if(line.find("Drone") != string::npos && cell[0] == 'A'){
            int i = cell[1]-'0';
            getline(s, cell, ',');
            drone_params[i].a = stof(cell);
        }else if(line.find("Drone") != string::npos && cell[0] == 'B'){
            int i = cell[1]-'0';
            getline(s, cell, ',');
            drone_params[i].b = stof(cell);
        }else if(line.find("Drone") != string::npos && cell[0] == 'C'){
            int i = cell[1]-'0';
            getline(s, cell, ',');
            drone_params[i].c = stof(cell);
        }else if(line.find("Drone") != string::npos && line.find("DT") != string::npos && line.find("Count") != string::npos){
            int i = cell[2]-'0';
            getline(s, cell, ',');
            drone_params[i].count = stoi(cell);
        }
    }

}

void init(){
    init_item_params();
    init_drone_params();
    init_recharge_params();
    deliveries = inp_deliveries();
    inp_parameters();
}