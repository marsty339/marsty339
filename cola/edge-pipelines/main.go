package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/katanomi/builds/pkg/apis/builds/v1alpha1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/dynamic"
	ctrl "sigs.k8s.io/controller-runtime"
)

func listBuildRuns(ctx context.Context, client dynamic.Interface, namespace string) (*v1alpha1.BuildRunList, error) {
	list, err := client.Resource(gvr).Namespace(namespace).List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		return nil, err
	}
	data, err := list.MarshalJSON()
	if err != nil {
		return nil, err
	}
	var brList v1alpha1.BuildRunList
	if err := json.Unmarshal(data, &brList); err != nil {
		return nil, err
	}
	return &brList, nil
}

func patchBuildRun(ctx context.Context, client dynamic.Interface, namespace, name string, pt types.PatchType, data []byte) error {
	fmt.Printf("canceled buildrun: %s\n", name)
	_, err := client.Resource(gvr).Namespace(namespace).Patch(ctx, name, pt, data, metav1.PatchOptions{})
	return err
}

var gvr = schema.GroupVersionResource{
	Group:    "builds.katanomi.dev",
	Version:  "v1alpha1",
	Resource: "buildruns",
}

func main() {
	ctx := context.Background()
	//TODO: use in-cluster mode
	config := ctrl.GetConfigOrDie()
	dyClient := dynamic.NewForConfigOrDie(config)

	namespace := "frontend-dev"
	items, err := listBuildRuns(ctx, dyClient, namespace)

	buildruns := make(map[string][]v1alpha1.BuildRun)

	// get running buildruns and sort by git PR id
	if err == nil {
		for _, item := range items.Items {
			// append running PR buildrun to list
			if item.Status.CompletionTime == nil && item.Status.Git.PullRequest != nil {
				//fmt.Println(namespace + "/" + item.Spec.BuildRef.Name + "/" + item.Spec.Git.Revision)
				key := namespace + "/" + item.Spec.BuildRef.Name + "/" + item.Spec.Git.Revision
				buildruns[key] = append(buildruns[key], item)
			}
		}
	} else {
		fmt.Println(err)
	}

	for _, brs := range buildruns {
		for i, j := 0, len(brs)-1; i < j; {
			var tmp v1alpha1.BuildRun
			var patchData string
			if brs[i].Status.StartTime.Before(brs[j].Status.StartTime) {
				tmp = brs[i]
				patchData = fmt.Sprintf(`{"spec": {"status" : "PipelineRunCancelled"}, "metadata": {"annotations": {"customize.katanomi.dev/cancel.reason": "older than buildrun: %s"}}}`, brs[j].Name)
				i++
			} else {
				tmp = brs[j]
				patchData = fmt.Sprintf(`{"spec": {"status" : "PipelineRunCancelled"}, "metadata": {"annotations": {"customize.katanomi.dev/cancel.reason": "older than buildrun: %s"}}}`, brs[i].Name)
				j--
			}
			errors := patchBuildRun(ctx, dyClient, namespace, tmp.Name, types.MergePatchType, []byte(patchData))
			if errors != nil {
				fmt.Println(errors)
			}
		}
	}
}
