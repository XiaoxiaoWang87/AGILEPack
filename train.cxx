#include "AGILEPack"
#include "parser.hh"
#include "struct_generator.hh"
#include <time.h>


#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "TH1.h"
#include "TFile.h"
#include "TString.h"
#include "TBranch.h"
#include "TTree.h"
#include "TAxis.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include "TRandom3.h"

//optionparser::parser generate_parser();

using namespace std;

class hist_class {

	public:
                hist_class(string sel, string Outfile, string Outdir);
		void Delete();
		void Write();

		TH1F* h_NN_train_sig;
		TH1F* h_NN_train_bkg;
                TH1F* h_NN_validate_sig;
                TH1F* h_NN_validate_bkg;
                TH1F* h_NN_evaluate_sig;
                TH1F* h_NN_evaluate_bkg;

                TH1F* h_NN_evaluate_sig_mt_cut;
                TH1F* h_NN_evaluate_bkg_mt_cut;

		TH1F* h_mt_evaluate_sig;
		TH1F* h_mt_evaluate_bkg;

	private: 
		string _outfile = "test";
		string _outdir = ".";
};

hist_class::hist_class(std::string sel, string Outfile, string Outdir){

	_outfile = Outfile;
	_outdir = Outdir;

	h_NN_train_sig = new TH1F((TString)("h_NN_train_sig_"+sel), (TString)("h_NN_train_sig_"+sel), 50, 0.25, 0.9);   h_NN_train_sig->Sumw2();
        h_NN_train_bkg = new TH1F((TString)("h_NN_train_bkg_"+sel), (TString)("h_NN_train_bkg_"+sel), 50, 0.25, 0.9);   h_NN_train_bkg->Sumw2();
        h_NN_validate_sig = new TH1F((TString)("h_NN_validate_sig_"+sel), (TString)("h_NN_validate_sig_"+sel), 50, 0.25, 0.9);   h_NN_validate_sig->Sumw2();
        h_NN_validate_bkg = new TH1F((TString)("h_NN_validate_bkg_"+sel), (TString)("h_NN_validate_bkg_"+sel), 50, 0.25, 0.9);   h_NN_validate_bkg->Sumw2();
        h_NN_evaluate_sig = new TH1F((TString)("h_NN_evaluate_sig_"+sel), (TString)("h_NN_evaluate_sig_"+sel), 50, 0.25, 0.9);   h_NN_evaluate_sig->Sumw2();
        h_NN_evaluate_bkg = new TH1F((TString)("h_NN_evaluate_bkg_"+sel), (TString)("h_NN_evaluate_bkg_"+sel), 50, 0.25, 0.9);   h_NN_evaluate_bkg->Sumw2();

        h_NN_evaluate_sig_mt_cut = new TH1F((TString)("h_NN_evaluate_sig_mt_cut_"+sel), (TString)("h_NN_evaluate_sig_mt_cut_"+sel), 50, 0.25, 0.9); h_NN_evaluate_sig_mt_cut->Sumw2();
        h_NN_evaluate_bkg_mt_cut = new TH1F((TString)("h_NN_evaluate_bkg_mt_cut_"+sel), (TString)("h_NN_evaluate_bkg_mt_cut_"+sel), 50, 0.25, 0.9); h_NN_evaluate_bkg_mt_cut->Sumw2();

	h_mt_evaluate_sig = new TH1F((TString)("h_mt_evaluate_sig_"+sel), (TString)("h_mt_evaluate_sig_"+sel), 30, 60, 300); h_mt_evaluate_sig->Sumw2(); 
	h_mt_evaluate_bkg = new TH1F((TString)("h_mt_evaluate_bkg_"+sel), (TString)("h_mt_evaluate_bkg_"+sel), 30, 60, 300); h_mt_evaluate_bkg->Sumw2();

  	return;
}

void hist_class::Write(){

	TString file_name = _outdir+"/"+_outfile+".root";

        TFile *my_out_file = new TFile(file_name, "RECREATE");

	h_NN_train_sig->Write();
	h_NN_train_bkg->Write();
	h_NN_validate_sig->Write();
	h_NN_validate_bkg->Write();
	h_NN_evaluate_sig->Write();
	h_NN_evaluate_bkg->Write();

        h_NN_evaluate_sig_mt_cut->Write();
        h_NN_evaluate_bkg_mt_cut->Write();

	h_mt_evaluate_sig->Write();
	h_mt_evaluate_bkg->Write();

        my_out_file->Close();

        return;
}

void hist_class::Delete(){

        delete h_NN_train_sig;
        delete h_NN_train_bkg;
        delete h_NN_validate_sig;
        delete h_NN_validate_bkg;
        delete h_NN_evaluate_sig;
        delete h_NN_evaluate_bkg;

        delete h_NN_evaluate_sig_mt_cut;
        delete h_NN_evaluate_bkg_mt_cut;

	delete h_mt_evaluate_sig;
	delete h_mt_evaluate_bkg;

	return;
}




class AGILE{

	private: 
		agile::root::tree_reader reader;
		agile::dataframe D;
		agile::neural_net my_net;

		agile::root::tree_reader reader_2;
		agile::root::tree_reader reader_3;

		float _unsupervised_learning_rate = 0.05;
		float _supervised_learning_rate = 0.0001;
		string _outfile = "test"; 
		string _outdir = ".";

		hist_class *hists; 

	public:
   		AGILE(float UnsupervisedLearningRate, float SupervisedLearningRate, string Outfile, string Outdir);
   		~AGILE();

		void init();
		void train();
		void validate();
		void evaluate();		
		void write();

};


AGILE::AGILE(float UnsupervisedLearningRate, float SupervisedLearningRate, string Outfile, string Outdir){

	_unsupervised_learning_rate = UnsupervisedLearningRate;
	_supervised_learning_rate = SupervisedLearningRate;
	_outfile = Outfile;
	_outdir = Outdir;
 
        hists = new hist_class("preselection", _outfile, _outdir);   	
}

AGILE::~AGILE(){

}

void AGILE::init(){
  
        reader.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "trainDL"); 

        reader.set_branch("Signal", agile::root::integer);
        reader.set_branch("EventWeight", agile::root::double_precision);

        //reader.set_branch("cutBTag70", agile::root::integer);
        //reader.set_branch("Tauveto", agile::root::integer);

        reader.set_branch("MET", agile::root::double_precision);
        reader.set_branch("mTW", agile::root::double_precision);
        //reader.set_branch("HT", agile::root::double_precision);
        //reader.set_branch("HTratio", agile::root::double_precision);
        //reader.set_branch("METsig", agile::root::double_precision);
        reader.set_branch("HTmissSig", agile::root::double_precision);
        reader.set_branch("aMT2", agile::root::double_precision);
        //reader.set_branch("MT2tau", agile::root::double_precision);
        reader.set_branch("Topness", agile::root::double_precision);
        reader.set_branch("Jet1_Pt", agile::root::double_precision);
        reader.set_branch("Jet2_Pt", agile::root::double_precision);
        reader.set_branch("Jet3_Pt", agile::root::double_precision);
        reader.set_branch("Jet4_Pt", agile::root::double_precision);
        reader.set_branch("Jet1_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet2_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet3_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet4_dPhiMET", agile::root::double_precision);
        //reader.set_branch("Lepton_BTag70Jet_mindR", agile::root::double_precision);
        reader.set_branch("Lepton_BMV1Jet_dR", agile::root::double_precision);
        reader.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader.set_branch("TrimmedJet1_4VM", agile::root::double_precision);
        //reader.set_branch("TrimmedJet2_dPhiMET", agile::root::double_precision);

        D = reader.get_dataframe(-1);

        D.to_csv(_outdir+"/"+_outfile+"_"+"data.csv");

        my_net.add_data(std::move(D));

        //my_net.model_formula("Signal ~ * | EventWeight");
	my_net.model_formula("Signal ~ * -EventWeight");


        reader_2.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "validateDL");

        reader_2.set_branch("Signal", agile::root::integer);
        reader_2.set_branch("EventWeight", agile::root::double_precision);

        reader_2.set_branch("MET", agile::root::double_precision);
        reader_2.set_branch("mTW", agile::root::double_precision);
        reader_2.set_branch("HTmissSig", agile::root::double_precision);
        reader_2.set_branch("aMT2", agile::root::double_precision);
        reader_2.set_branch("Topness", agile::root::double_precision);
        reader_2.set_branch("Jet1_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet2_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet3_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet4_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet1_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet2_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet3_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet4_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Lepton_BMV1Jet_dR", agile::root::double_precision);
        reader_2.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_4VM", agile::root::double_precision);


        reader_3.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "evaluateDL");

        reader_3.set_branch("Signal", agile::root::integer);
        reader_3.set_branch("EventWeight", agile::root::double_precision);

        reader_3.set_branch("MET", agile::root::double_precision);
        reader_3.set_branch("mTW", agile::root::double_precision);
        reader_3.set_branch("HTmissSig", agile::root::double_precision);
        reader_3.set_branch("aMT2", agile::root::double_precision);
        reader_3.set_branch("Topness", agile::root::double_precision);
        reader_3.set_branch("Jet1_Pt", agile::root::double_precision);
        reader_3.set_branch("Jet2_Pt", agile::root::double_precision);
        reader_3.set_branch("Jet3_Pt", agile::root::double_precision);
        reader_3.set_branch("Jet4_Pt", agile::root::double_precision);
        reader_3.set_branch("Jet1_dPhiMET", agile::root::double_precision);
        reader_3.set_branch("Jet2_dPhiMET", agile::root::double_precision);
        reader_3.set_branch("Jet3_dPhiMET", agile::root::double_precision);
        reader_3.set_branch("Jet4_dPhiMET", agile::root::double_precision);
        reader_3.set_branch("Lepton_BMV1Jet_dR", agile::root::double_precision);
        reader_3.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader_3.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader_3.set_branch("TrimmedJet1_4VM", agile::root::double_precision);


}


void AGILE::train(){

        //my_net.emplace_back(new autoencoder(16, 30, sigmoid, linear));
        my_net.emplace_back(new autoencoder(17, 30, sigmoid, linear));
        my_net.emplace_back(new autoencoder(30, 12, sigmoid, sigmoid));

        //my_net.emplace_back(new autoencoder(16, 17, sigmoid, linear));
        //my_net.emplace_back(new autoencoder(17, 12, sigmoid, sigmoid)); 
        my_net.emplace_back(new autoencoder(12, 5, sigmoid, sigmoid));
        my_net.emplace_back(new autoencoder(5, 3, sigmoid, sigmoid)); 
        my_net.emplace_back(new layer(3, 1, sigmoid)); 
        
        my_net.set_learning(_unsupervised_learning_rate); //(0.05);

        my_net.set_regularizer(0.001);
        my_net.set_batch_size(1);
        my_net.check(); // checks the dimensions on the network
        
        my_net.train_unsupervised(10);

        my_net.set_learning(_supervised_learning_rate);//(0.0001);
        my_net.train_supervised(10);

        my_net.to_yaml(_outdir + "/" +_outfile + ".yaml", reader.get_var_types());




	// filling training data histograms
        my_net.from_yaml(_outdir + "/" +_outfile + ".yaml");

        int n_events = reader.size();
        cout<< n_events <<endl;

        auto input_variables = reader.get_ordered_branch_names();    //my_net.get_inputs();
        cout<< input_variables.size() <<endl;

        for (int evt = 0; evt < n_events; ++evt){

                std::map<std::string, double> var = reader(evt, input_variables);

                auto predictions = my_net.predict_map(var); //(reader(evt, input_variables));
                //cout << predictions["Signal"] << endl;
                //cout<<var["Signal"]<<endl;
                //cout<<var["MET"]<<endl;
                if(var["Signal"]==1) hists->h_NN_train_sig->Fill(predictions["Signal"], 1.0);
                else hists->h_NN_train_bkg->Fill(predictions["Signal"], 1.0);
        }

}


void AGILE::validate(){

	// filling validation data histograms
        my_net.from_yaml(_outdir + "/" +_outfile + ".yaml");

        int n_events = reader_2.size();
        cout<< n_events <<endl;

        auto input_variables = reader_2.get_ordered_branch_names();    //my_net.get_inputs();
        cout<< input_variables.size() <<endl;

        for (int evt = 0; evt < n_events; ++evt){

                std::map<std::string, double> var = reader_2(evt, input_variables);

                auto predictions = my_net.predict_map(var); //(reader_2(evt, input_variables));
                //cout << predictions["Signal"] << endl;
                //cout<<var["Signal"]<<endl;
                //cout<<var["MET"]<<endl;
                if(var["Signal"]==1) hists->h_NN_validate_sig->Fill(predictions["Signal"], 1.0);
                else hists->h_NN_validate_bkg->Fill(predictions["Signal"], 1.0);
        }

}

void AGILE::evaluate(){

	// filling evaluating data histograms
	my_net.from_yaml(_outdir + "/" +_outfile + ".yaml");

	int n_events = reader_3.size();
	cout<< n_events <<endl;

        auto input_variables = reader_3.get_ordered_branch_names();    //my_net.get_inputs();
	cout<< input_variables.size() <<endl;

        //for (int evt = 0; evt < 10; ++evt){ 
	for (int evt = 0; evt < n_events; ++evt){

                std::map<std::string, double> var = reader_3(evt, input_variables);

                auto predictions = my_net.predict_map(var); //(reader_3(evt, input_variables));
                //cout << predictions["Signal"] << endl;
		//cout<<var["Signal"]<<endl;
                //cout<<var["MET"]<<endl;
                if(var["Signal"]==1) {
			hists->h_NN_evaluate_sig->Fill(predictions["Signal"], var["EventWeight"]);
                        if(var["mTW"]>125) hists->h_NN_evaluate_sig_mt_cut->Fill(predictions["Signal"], var["EventWeight"]);
			if(predictions["Signal"] > 0.75) hists->h_mt_evaluate_sig->Fill(var["mTW"], var["EventWeight"]);
		}
                else {
			hists->h_NN_evaluate_bkg->Fill(predictions["Signal"], var["EventWeight"]);
                        if(var["mTW"]>125) hists->h_NN_evaluate_bkg_mt_cut->Fill(predictions["Signal"], var["EventWeight"]);
			if(predictions["Signal"] > 0.75) hists->h_mt_evaluate_bkg->Fill(var["mTW"], var["EventWeight"]);
		}
        }


}



void AGILE::write(){

	hists->Write();
	hists->Delete();

}







int main(int argc, char const *argv[])
{

	string outfile = "test";
	string outdir = ".";
	float unsupervised_learning_rate = 0.05;
	float supervised_learning_rate = 0.0001;
	

	if(argc < 2) {
		cout<<"use default arguments"<<endl;
	}
	else if(argc==5){
		cout<<"use user defined arguments"<<endl;
		unsupervised_learning_rate = atof(argv[1]);
		supervised_learning_rate = atof(argv[2]);
		outfile = argv[3];
		outdir = argv[4];
	}
	else{
		cout<<"too few or too many arguments"<<endl;
		exit(1);
	}

        //auto p = generate_parser();
        //p.eat_arguments(argc, argv);

        //std::vector<std::string> root_files(p.get_value<std::vector<std::string>>("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140711_DL/mergeDL.root"));
        //int start = p.get_value<int>("start"), end = p.get_value<int>("end");
        //
        //std::count<<"start: "<< start << std::endl;
        //std::count<<"end: "<< end << std::endl;
/*
	agile::root::tree_reader reader;
	
	reader.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "train"); 

	reader.set_branch("Signal", agile::root::integer);
        //reader.set_branch("EventWeight", agile::root::double_precision);

        //reader.set_branch("cutBTag70", agile::root::integer);
        //reader.set_branch("Tauveto", agile::root::integer);

        reader.set_branch("MET", agile::root::double_precision);
        //reader.set_branch("mTW", agile::root::double_precision);
        //reader.set_branch("HT", agile::root::double_precision);
        //reader.set_branch("HTratio", agile::root::double_precision);
        //reader.set_branch("METsig", agile::root::double_precision);
        reader.set_branch("HTmissSig", agile::root::double_precision);
        reader.set_branch("aMT2", agile::root::double_precision);
        //reader.set_branch("MT2tau", agile::root::double_precision);
        reader.set_branch("Topness", agile::root::double_precision);
        reader.set_branch("Jet1_Pt", agile::root::double_precision);
        reader.set_branch("Jet2_Pt", agile::root::double_precision);
        reader.set_branch("Jet3_Pt", agile::root::double_precision);
        reader.set_branch("Jet4_Pt", agile::root::double_precision);
        reader.set_branch("Jet1_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet2_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet3_dPhiMET", agile::root::double_precision);
        reader.set_branch("Jet4_dPhiMET", agile::root::double_precision);
        //reader.set_branch("Lepton_BTag70Jet_mindR", agile::root::double_precision);
        reader.set_branch("Lepton_BMV1Jet_dR", agile::root::double_precision);
        reader.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader.set_branch("TrimmedJet1_4VM", agile::root::double_precision);
        //reader.set_branch("TrimmedJet2_dPhiMET", agile::root::double_precision);

	
	agile::dataframe D = reader.get_dataframe(-1);

        agile::root::tree_reader reader_2;
        reader_2.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140727_DL/mergeDL.root", "evaluate");
	
	reader_2.set_branch("Signal", agile::root::integer);
	//reader_2.set_branch("EventWeight", agile::root::double_precision);
	
 	reader_2.set_branch("MET", agile::root::double_precision);
        reader_2.set_branch("HTmissSig", agile::root::double_precision);
        reader_2.set_branch("aMT2", agile::root::double_precision);
	reader_2.set_branch("Topness", agile::root::double_precision);
        reader_2.set_branch("Jet1_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet2_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet3_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet4_Pt", agile::root::double_precision);
        reader_2.set_branch("Jet1_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet2_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet3_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Jet4_dPhiMET", agile::root::double_precision);
        reader_2.set_branch("Lepton_BMV1Jet_dR", agile::root::double_precision);
        reader_2.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_4VM", agile::root::double_precision);
	

        D.to_csv("data.csv");

	agile::neural_net my_net;
	
	my_net.add_data(std::move(D));
	
	my_net.model_formula("Signal ~ *"); 
	
	my_net.emplace_back(new autoencoder(16, 17, sigmoid, linear));
	my_net.emplace_back(new autoencoder(17, 12, sigmoid, sigmoid)); 
	my_net.emplace_back(new autoencoder(12, 5, sigmoid, sigmoid));
	my_net.emplace_back(new autoencoder(5, 3, sigmoid, sigmoid)); 
	my_net.emplace_back(new layer(3, 1, sigmoid)); 
	
	my_net.set_learning(0.05);
	my_net.set_regularizer(0.001);
	my_net.set_batch_size(1);
	my_net.check(); // checks the dimensions on the network
	
	my_net.train_unsupervised(10);

	//my_net.set_learning(0.01);
        my_net.set_learning(0.0001);
	my_net.train_supervised(10);

	my_net.to_yaml("test.yaml", reader.get_var_types());



	hist_class *hists = new hist_class("preselection");

        
        auto input_variables = my_net.get_inputs();
        for (int evt = 0; evt < 711866; ++evt){

		std::map<std::string, double> var = reader_2(evt, input_variables);

		auto predictions = my_net.predict_map(var); //(reader_2(evt, input_variables));
		std::cout << predictions["Signal"] << std::endl;
                if(var["Signal"]==1) hists->h_NN_sig->Fill(predictions["Signal"], 1.0);
		else hists->h_NN_bkg->Fill(predictions["Signal"], 1.0);
        }

	hists->Write();
        hists->Delete();

*/


	AGILE agile(unsupervised_learning_rate, supervised_learning_rate, outfile, outdir);

	agile.init();
        agile.train();

	agile.validate();
	agile.evaluate();

	agile.write();

	return 0;

}
