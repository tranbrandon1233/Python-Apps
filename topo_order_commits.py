# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.
import os, sys, zlib
def topo_order_commits():
        
    git_found = False
    while os.getcwd() != "/":   #Continue looping until root dir is reached
        for x in os.listdir(os.getcwd()):  #Check each file in directory
            if x == ".git":   #Find .git dir
                git_found = True
                print("The .git directory is is at " + os.getcwd())
                os.chdir(".git")
                class CommitNode:   #CommitNode class
                    def __init__(self, commit_hash):  #Initialization function
                        """
                        :type commit_hash: str
                        """
                        self.commit_hash = commit_hash
                        self.parents = set()
                        self.children = set()
                        #Find parents
                        os.system("git cat-file -p "+self.commit_hash + " > output.txt")   #Send information of commit to text file
                        file = open("output.txt")
                        line=file.readline()  #Open and read the text file
                        while line != '':
                            index = line.find('parent')  #Find the parent hash from text
                            if index != -1:   
                                self.parents.add(line[7:len(line)-1])   #Add to parents set
                            line=file.readline()   #Move onto next line
                        file.close()   #Close and remove file
                        os.system("rm output.txt")

                        #Find children
                        os.system("git log --ancestry-path --format=%H " + self.commit_hash +"..master | tail -1 > output.txt") #Send information of commit's children to text file   
                        file = open("output.txt") #Open and read the text file
                        line=file.readline()
                        index = line.find(' ')  #See if there are multiple children
                        if index == -1:   #If not,
                            self.children.add(line[1:len(line)])  #Store hash of child in children set
                        else:
                            self.children.add(line[1:index-1])  
           
                        while index != -1:   #Loop until new child not found
                            new_line = line[index+1:len(line)]  #Search if another child exists
                            next_index = new_line.find(" ")
                            if next_index != -1:   #If so,
                                self.parents.add(line[index+1:next_index-1])  #Store previously found child
                            else:
                                self.parents.add(line[index+1:len(line)])  #Store rest of line
                            index = next_index
                        file.close()   #Close and remove file
                        os.system("rm output.txt")


                    

                nodes_queue = []  #Initialization
                ordered_q = []
                used_nodes = []
                root_commits = []
                node = CommitNode("46fbca76b2f65a52fd0dca044a666d073277e0d1")
                while len(node.parents) != 0:  #Repeat for all nodes
                    child_found = False
                    if len(node.children) == 0:  #For all leaf nodes
                        nodes_queue.append(node.commit_hash)  #Add nodes to queues
                        ordered_q.append(nodes_queue.pop())
                        used_nodes.append(node.commit_hash)
                        root_commits.append(node.commit_hash)
                    else:
                        for child in node.children:   #Find if any children still need to be added to queues
                            if child not in used_nodes:
                                node = CommitNode(child)
                                child_found = True
                                break
                        if child_found:  #If so,
                            continue  #Break from loop to process child
                        else:
                            nodes_queue.append(node.commit_hash)  #Add nodes to queue in correct order
                            ordered_q.append(nodes_queue.pop())
                            used_nodes.append(node.commit_hash)
                    for parent in node.parents:   
                        if parent not in used_nodes:
                            node = CommitNode(parent)  #Move on to parent node
                if len(node.parents) == 0:
                    nodes_queue.append(node.commit_hash)  #Add nodes to queue in correct order
                    ordered_q.append(nodes_queue.pop())
                    used_nodes.append(node.commit_hash)
                    root_commits.append(node.commit_hash)
        if git_found:  
            break
        else:
           os.chdir('../')  #Move to next dir if .git not found
    if (not git_found):
        sys.stderr("Not inside a Git repository")   #Error message if .git not found
        exit(1)

#I tried to use strace to verify the function does not use other commands, but the terminal could not find the file even when it was in the same directory

if __name__ == '__main__':
    topo_order_commits()
