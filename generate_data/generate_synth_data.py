import torchio as tio
import commentjson as json


#function to parse the json parameter and construct the corresponding torchio transform
def get_transform_from_json(json_file):
    with open(json_file) as f:
        transfo_st = json.load(f)

    return parse_transform(transfo_st['train_transforms'])


def parse_transform(t):
    if isinstance(t, list):
        transfo_list = [parse_transform(tt) for tt in t]
        return tio.Compose(transfo_list)


    attributes = t.get('attributes') or {}

    t_class = getattr(tio.transforms, t['name'])
    return t_class(**attributes)


#addapt the path
root_data_path = '/data/romain/toolbox_python/romain/Synth_baby/'

file_transfo_json = root_data_path + 'transform.json'
label_data_list = [ root_data_path + 'sub-CC00154XX06_iWMnw_drawem9_mida_ext_thin_dseg.nii.gz', 
                    root_data_path + 'sub-CC00694XX19_iWMnw_drawem9_mida_ext_thin_dseg.nii.gz']


#get the transform
tio_transfo = get_transform_from_json(file_transfo_json)

#construct a torchio dataset given a list of label files

#create a torchio subject list
subject_list=[]
for k, label_file in enumerate(label_data_list) :
    sujname = f'Suj_{k:02}'
    #note the "label" tag is consistent with "label_key" define the RandomLabelsToImage transform
    suj = tio.Subject(name=sujname, label=tio.LabelMap(label_file) )
    
    subject_list.append(suj)

    
tioDS = tio.SubjectsDataset( subject_list, transform=tio_transfo )

#generate
output_dir = root_data_path + '/generate_data/'
nb_example_per_subject = 2

for ngen in range(nb_example_per_subject):
    print(f'Pass {ngen+1}')
    for suj in tioDS:
        print(f'Subject {suj.name}')
        outdir_name_data  = output_dir + f'gen{ngen:02}_{suj.name}_synthdata.nii.gz'
        outdir_name_label = output_dir + f'gen{ngen:02}_{suj.name}_target.nii.gz'        

        #as define in RandomLabelsToImage the synthetic image is name t1
        suj.t1.save(outdir_name_data)        
        suj.label.save(outdir_name_label)
    
    
