import sys
import subprocess



def extract_baremetal_installer(work_dir, openshift_release_image):
    try:
        command = "{oc_dir}/oc adm release extract --command=openshift-baremetal-install  --to={out_dir} {release_image}".format(
            oc_dir=work_dir, out_dir=work_dir, release_image=openshift_release_image)
        subprocess.check_output(command, shell=True, stderr=sys.stdout)
    except Exception as ex:
        raise Exception('Failed to extract installer, exception: {}'.format(ex))


def get_mco_image(work_dir, openshift_release_image):
    try:
        command = "{oc_dir}/oc adm release info {release_image} --pullspecs | grep machine-config-operator".format(
            oc_dir=work_dir, release_image=openshift_release_image)
        res = subprocess.check_output(command, shell=True, stderr=sys.stdout).decode('utf-8')
        return res.split()[1]
    except Exception as ex:
        raise Exception('Failed to extract MCO image, exception: {}'.format(ex))
