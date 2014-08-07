#include "AGILEPack"
#include "parser.hh"
#include "struct_generator.hh"
#include <time.h>

int main(int argc, char const *argv[])
{

        agile::root::tree_reader reader_2;
        reader_2.add_file("/group/atlas/data/D3PDs/xwang/1LStopBoosted/plot_output/20140711_DL/merge.root", "evaluate");

        reader_2.set_branch("Signal", agile::root::integer);

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
        reader_2.set_branch("Lepton_TrimmedJet1_dR", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_Pt", agile::root::double_precision);
        reader_2.set_branch("TrimmedJet1_4VM", agile::root::double_precision);


	agile::neural_net ARCH;
	ARCH.from_yaml("test.yaml");
	 
        auto input_variables = ARCH.get_inputs();
        //auto output_variables = ARCH.get_outputs();

        std::cout<< input_variables.size() << std::endl;
        for (int t = 0; t < 15; t++){
             std::cout<< input_variables[t] << std::endl;
        }

	for (int point = 0; point < 10000; ++point)
	{
	  //std::map<string,double> thismap = reader_2(point, input_variables);
          //std::cout<< reader_2(point, input_variables)["MET"] << std::endl;

	  auto r = ARCH.predict_map(reader_2(point, input_variables));
  
	  std::cout<< r["Signal"] <<std::endl;  
	  //auto o = reader_2(point, ARCH.get_outputs());
          //std::cout<< o <<std::endl;
	  //std::cout << "predicted:\n" << r << "\nactual:\n" << o << std::endl;
	}
   
}   
